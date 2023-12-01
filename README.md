# Bluefors API with python

This repo helps you collect all relevant temperatures from Bluefors LD250 control unit.  
All updates on the temperatures are run asynchronously.  
Will include pressure reading, pumps status and valve status in the future.

You will need:
- python >= 3.4
- websockets

json is included in python since 2.6
and asyncio since 3.4

``` 
pip install websockets
```

Or

``` 
conda install -c conda-forge websockets
```

## Simple example

``` python
from ld250 import Temperatures

temperatures = Temperatures(port = 49099)

last_temperatures = temperatures.get_temperatures()
for key in last_temperatures:
    temperature =  last_temperatures[key]
    temperature_rounded = round(temperature, 1)
    print(f"{key}\t=\t{temperature_rounded}\tK")
```

### Output
```
t50k    =       55.2     K
t4k     =       15.7     K
tmagnet =       16.2     K
tstill  =       18.8     K
tmixing =       19.5     K
tfse    =       25.3     K
```