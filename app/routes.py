from flask import Blueprint, jsonify

weather_routes = Blueprint('weather_api', __name__)

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


@weather_routes.route('/health_check', methods=['GET'])
def health_check():
    return jsonify({"status": "OK"}), 200

@weather_routes.route('/<city_name>', methods=['GET'])
def get_weather(city_name: str):
    city_weather = mock_data.get(city_name)
    if not city_weather:
        return jsonify({"error": "City not found"}), 404
    return jsonify(city_weather), 200