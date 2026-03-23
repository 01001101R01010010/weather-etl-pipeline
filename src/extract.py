import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
CITIES = ["Warsaw", "Krakow", "Gdansk", "Wroclaw", "Poznan"]
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def fetch_weather(city: str) -> dict | None:
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "pl"
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Błąd pobierania danych dla {city}: {e}")
        return None

def extract_all_cities() -> list[dict]:
    raw_data = []
    for city in CITIES:
        data = fetch_weather(city)
        if data:
            raw_data.append(data)
            print(f"✓ Pobrano dane dla {city}")
    return raw_data