import requests

def get_weather(country, city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid=1508a9a4840a5574c822d70ca2132032' 
    r = requests.get(url)
    weather_city_founded = r.json()
    
    return weather_city_founded