import json
from datetime import datetime


wind_dictionary_all_days = str(datetime.now())
print(wind_dictionary_all_days)

with open("test.json", "r") as file_load:
    wind_dictionary_all_days = str(wind_dictionary_all_days)

with open("test.json", "w") as weather_dump:
    json.dump(wind_dictionary_all_days, weather_dump)
