import asyncio
import websockets
import json

class Temperatures(object):
    """
    Class that collect all relevant temperatures from
    Bluefors LD250 control unit.
    Opens an asynchronous websocket in listener mode
    for all temperatures in the system.
    Temperatures can be pulled with the get_temperature method.
    Attributes:
        port:   the port through which the websocket is open.
                default port number on LD250 is 49099 for unsecure ws
    """
    def __init__(self, port = 49099) -> None:
        self.port = port
        self._addr = f"ws://localhost:{self.port}/ws/values/?"
        self._temperatures = {}
        self._initial_temperature_reading()
        self._start_temperature_update_loop()
    
    def get_temperatures(self):
        """Returns a dictionary containing all temperatures monitored
        by the bluefors control unit. 
        The keys are the names given to those temperatures by the
        control unit.
        """
        return self._temperatures

    def _initial_temperature_reading(self):
        ini_loop = asyncio.get_event_loop()
        ini_loop.run_until_complete(self._initialiaze_temperatures())
        ini_loop.close()

    def _start_temperature_update_loop(self):
        self._run_updates = True
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._task = self._loop.create_task(self._continuous_updates())
    
    def __del__(self):
        self._stop()

    def _stop(self):
        if self._task:
            self._run_updates = False
            self._loop.run_until_complete(self._task)
            self._task.cancel()
            self._task = None
        self._loop.close()    

    async def _initialiaze_temperatures(self):
        input = {
            "command" : "read",
            "data" : {
                "target" : "mapper.bf.temperatures",
                "recursion" : "1",
                    },
        }
        async with websockets.connect(self._addr) as websocket:
            await websocket.send(json.dumps(input))
            #get the received message
            response = await websocket.recv()
            #get the data
            response = await websocket.recv()
            self._update_temperatures_from_json(response)

    async def _continuous_updates(self):
        input = {
            "command" : "listen",
            "data" : {
                "target" : "mapper.bf.temperatures",
                "recursion" : "true",
                    },
        }
        async with websockets.connect(self._addr) as websocket:
            await websocket.send(json.dumps(input))
            #get the received message
            response = await websocket.recv()
            #get the succeed message
            response = await websocket.recv()
            #get the notifications
            while self._run_updates:
                response = await websocket.recv()
                self._update_temperatures_from_json(response)

    def _update_temperatures_from_json(self,response):
        response = json.loads(response)
        data = response["data"]
        for key in data:
            self._update_temperature_from_json(data[key])

    def _update_temperature_from_json(self, data):
        if self._is_right_unit(data) is not True:
            return 0
        
        full_name = data["name"]
        t_name = full_name.split(".")[-1]

        value = self._extract_temperature(data)
        self._update_temperatures(t_name, value)
    
    def _is_right_unit(self, data):
        bf_type = data["type"]
        if bf_type == "Value.Number.Float.Unit.temperature":
            return True
        return False
    
    def _extract_temperature(self, data):
        content = data["content"]
        value_string = content["latest_value"]["value"]
        value = self._convert_value_string_to_float(value_string)
        return value
    
    def _convert_value_string_to_float(self, value_string):
        if value_string == "":
            value_string = "NaN"
        return float(value_string)
    
    def _update_temperatures(self, t_name, value):
        self._temperatures[t_name] = value