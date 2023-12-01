from ld250 import Temperatures

temperatures = Temperatures(port = 49099)

last_temperatures = temperatures.get_temperatures()
for key in last_temperatures:
    temperature =  last_temperatures[key]
    temperature_rounded = round(temperature, 1)
    print(f"{key}\t=\t{temperature_rounded}\tK")