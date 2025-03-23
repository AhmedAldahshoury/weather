import os
from typing import Optional

import requests

from app.constants import GEO_URL

API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")


def get_city_coordinates(city_name: str)-> Optional[tuple[float, float]]:
    params = {
        'q': city_name,
        'limit': 1,
        'appid': API_KEY
    }

    try:
        response = requests.get(GEO_URL, params=params)
        response.raise_for_status()

        data = response.json()

        if not data:
            print(f"No data found for city: {city_name}")
            return None

        city_data = data[0]
        latitude = city_data.get('lat')
        longitude = city_data.get('lon')

        return latitude, longitude

    except requests.RequestException as e:
        print(f"Error fetching city coordinates: {e}")
        return None