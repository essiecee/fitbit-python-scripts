import json
import requests
#import tractdb

print "this is the weather information for Seattle"
response = requests.get('http://api.openweathermap.org/data/2.5/weather?zip=98115,us&APPID=e26ae6838ed61b6d2d1bde8c00aaa3b5')
print(response.status_code)
data = response.json()
print(data)

print "this is the weather information for Sunnyvale"
response = requests.get("http://api.openweathermap.org/data/2.5/weather?zip=94088,us&APPID=e26ae6838ed61b6d2d1bde8c00aaa3b5")
print(response.status_code)
data = response.json()
print(data)

print "this is the weather information for NYC"
response = requests.get("http://api.openweathermap.org/data/2.5/weather?zip=10001,us&APPID=e26ae6838ed61b6d2d1bde8c00aaa3b5")
print(response.status_code)
data = response.json()
print(data)
