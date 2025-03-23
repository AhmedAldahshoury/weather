import os
from datetime import datetime
from typing import Optional

import click
import requests

from app import db
from app.constants import GEO_URL, FORECAST_URL
from app.models.models import Forecast, City

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


def populate_forecasts():
    cities = City.query.all()

    if not cities:
        click.echo("No cities found in the database.")
        return

    for city in cities:
        try:
            params = {
                "lat": city.latitude,
                "lon": city.longitude,
                "appid": API_KEY,
                "units": "metric"
            }

            response = requests.get(FORECAST_URL, params=params)
            response.raise_for_status()
            weather_data = response.json()

            forecasts = weather_data.get('list', [])

            if not forecasts:
                click.echo(f"No forecast data found for city: {city.name}")
                continue

            for forecast_data in forecasts:
                try:
                    forecast_datetime = datetime.strptime(forecast_data['dt_txt'], "%Y-%m-%d %H:%M:%S")
                    temperature = forecast_data['main']['temp']
                    humidity = forecast_data['main']['humidity']

                    condition = (forecast_data['weather'][0]['description']
                                 if 'weather' in forecast_data and forecast_data['weather'] else "Unknown")

                    wind_speed = (forecast_data['wind']['speed']
                                  if 'wind' in forecast_data else 0.0)

                    forecast = Forecast(
                        city_id=city.id,
                        date=forecast_datetime.date(),
                        temperature=temperature,
                        humidity=humidity,
                        condition=condition,
                        wind_speed=wind_speed
                    )

                    db.session.add(forecast)

                except KeyError as e:
                    click.echo(f"Missing data in forecast for city {city.name}: {e}")
                except Exception as e:
                    click.echo(f"Unexpected error while processing forecast for city {city.name}: {e}")

            db.session.commit()
            click.echo(f"Successfully populated forecasts for city: {city.name}")

        except requests.RequestException as e:
            db.session.rollback()
            click.echo(f"Failed to fetch data for city {city.name}: {e}")

        except Exception as e:
            db.session.rollback()
            click.echo(f"Error saving forecasts for city {city.name}: {e}")

def populate_db_with_cities(cities_list: list[dict[str,str]]):

    for city_info in cities_list:
        try:
            city_name = city_info.get('name')
            country_name = city_info.get('country')

            if not city_name or not country_name:
                continue

            if City.query.filter_by(name=city_name).first():
                continue

            latitude, longitude = get_city_coordinates(city_name)

            if not (latitude and longitude):
                continue

            new_city = City(name=city_name, country=country_name, latitude=latitude, longitude=longitude)
            db.session.add(new_city)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            click.echo(e)
