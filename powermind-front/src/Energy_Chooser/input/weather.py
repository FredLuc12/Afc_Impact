import requests
from src.Energy_Chooser.constant import url
from dotenv import load_dotenv
import os

load_dotenv()

def get_weather(city="Paris"):

    params = {
        "q": city,
        "appid": os.getenv("API_KEY_METO"),
        "units": "metric" 
    }

    response = requests.get(url.API_METEO, params=params)
    data = response.json()

    temp = data["main"]["temp"]

    return int(round(temp))
