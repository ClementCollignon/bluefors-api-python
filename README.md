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
    print(f"{key}\t=\t{last_temperatures[key]}\tK")
```