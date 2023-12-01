from ld250 import Temperatures

temperatures = Temperatures(port = 49099)

last_temperatures = temperatures.get_temperatures()
for key in last_temperatures:
    print(f"{key}\t=\t{last_temperatures[key]}\tK")
