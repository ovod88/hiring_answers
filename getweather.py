from pyowm import OWM 
import os
import json



API_key = os.environ['OPENWEATHER_API_KEY']
CITY = os.environ['CITY_NAME']

weather_own = OWM(API_key)

weather_obj = weather_own.weather_at_place(CITY)
weather_json_obj = json.loads(weather_obj.to_JSON())

# print(weather_obj.to_JSON()) 
# print(dir(weather_own))
# print(weather_own.get_subscription_type())
# print(weather_obj.get_weather().to_JSON())
# print(weather_obj['OWM_API_VERSION'])

result = """source=openweathermap, city=\"{city}\", description=\"{desc}\", temp={temp},
			humidity={hum}""".format(city=CITY, desc=weather_json_obj['Weather']['detailed_status'], \
							temp=weather_json_obj['Weather']['temperature']['temp'], \
							hum=weather_json_obj['Weather']['humidity'])

print(result)
# print(type(weather_json_obj))