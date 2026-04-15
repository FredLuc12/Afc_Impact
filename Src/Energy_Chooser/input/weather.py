import requests
from constant import url

def get_weather():
    temp = requests.get(url.API_METEO).text
    temp_formatted = temp.replace("Â°C", "").replace("°C", "").replace("+", "").strip()
    return temp_formatted