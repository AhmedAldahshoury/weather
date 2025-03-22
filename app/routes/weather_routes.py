from datetime import datetime

from flasgger import swag_from
from flask import Blueprint, jsonify
from ..models.models import Weather


mock_data = {
    "Vienna": [
        { "date": "2025-03-13", "temperature": "15°C", "humidity": "55%", "condition": "Sunny", "wind_speed": "10 km/h" },
        { "date": "2025-03-14", "temperature": "17°C", "humidity": "50%", "condition": "Partly Cloudy", "wind_speed": "12 km/h" }
    ],
    "Prague": [
        { "date": "2025-03-13", "temperature": "12°C", "humidity": "60%", "condition": "Cloudy", "wind_speed": "8 km/h" },
        { "date": "2025-03-14", "temperature": "14°C", "humidity": "55%", "condition": "Partly Cloudy", "wind_speed": "10 km/h" }
    ]
}

weather_routes = Blueprint('weather', __name__)

@weather_routes.route('/health_check', methods=['GET'])
def health_check():
    return jsonify({"status": "OK"}), 200


@weather_routes.route('/today', methods=['GET'])
def get_all_weather_today():
    try:
        today_date = datetime.today().strftime('%Y-%m-%d')
        weather_records = Weather.query.filter(Weather.date == today_date).all()
        results = [
                    {
                        'id': record.id,
                        'city': record.city_id,
                        'temperature': record.temperature,
                        'condition': record.condition,
                        'humidity': record.humidity,
                        'wind_speed': record.wind_speed,
                    }
                    for record in weather_records
                ]
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@weather_routes.route('/<city_name>', methods=['GET'])
@swag_from('../docs/get_city_weather.yml')
def get_city_weather(city_name: str):
    city_weather = mock_data.get(city_name)
    if not city_weather:
        return jsonify({'error': f'City "{city_name}" is not found'}), 404
    return jsonify(city_weather), 200

@weather_routes.route('/<city_name>/<date>', methods=['GET'])
@swag_from('../docs/get_city_weather_by_date.yml')
def get_city_weather_by_date(city_name: str, date: str):
    city_weather = mock_data.get(city_name)
    if not city_weather:
        return jsonify({'error': f'City "{city_name}" is not found'}), 404

    for weather_entry in city_weather:
        if weather_entry['date'] == date:
            return jsonify(weather_entry), 200

    return jsonify({'error': f'No weather info was found for "{city_name}" on "{date}"'}), 404
