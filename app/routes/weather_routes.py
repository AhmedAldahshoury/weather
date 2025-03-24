from datetime import datetime
from flask import Blueprint, jsonify, request
from flasgger import swag_from

from ..constants import DATE_FORMAT
from ..models.models import Forecast, City
from app import db

weather_bp = Blueprint('weather', __name__)


@weather_bp.route('/', methods=['POST'])
@swag_from('../docs/weather_swagger/create_forecast.yml')
def create_forecast():
    data = request.json
    if not data:
        return jsonify({'error': 'Request body must be JSON.'}), 400

    required_fields = ['city_name', 'date', 'temperature', 'humidity', 'condition', 'wind_speed']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400

    city_name = data.get('city_name')
    city = City.query.filter_by(name=city_name).first()
    if not city:
        return jsonify({'error': f'City {city_name} not found. Please create the city first.'}), 404

    try:
        new_forecast = Forecast(
            city_id=city.id,
            date=datetime.strptime(data['date'], DATE_FORMAT).date(),
            temperature=float(data['temperature']),
            humidity=float(data['humidity']),
            condition=data['condition'],
            wind_speed=float(data['wind_speed'])
        )
    except ValueError:
        return jsonify({'error': 'Invalid data format.'}), 400

    db.session.add(new_forecast)
    db.session.commit()

    return jsonify({'message': 'Forecast created successfully!'}), 201


@weather_bp.route('/', methods=['GET'])
@swag_from('../docs/weather_swagger/get_all_forecasts.yml')
def get_all_forecasts():
    forecasts = Forecast.query.all()
    result = [
        {
            'id': forecast.id,
            'city_id': forecast.city_id,
            'date': forecast.date.strftime(DATE_FORMAT),
            'temperature': forecast.temperature,
            'humidity': forecast.humidity,
            'condition': forecast.condition,
            'wind_speed': forecast.wind_speed
        } for forecast in forecasts
    ]
    return jsonify({'forecasts': result})


@weather_bp.route('/<int:forecast_id>', methods=['GET'])
@swag_from('../docs/weather_swagger/get_forecast_by_id.yml')
def get_forecast_by_id(forecast_id):
    forecast = Forecast.query.get_or_404(forecast_id)
    result = {
        'id': forecast.id,
        'city_id': forecast.city_id,
        'date': forecast.date.strftime(DATE_FORMAT),
        'temperature': forecast.temperature,
        'humidity': forecast.humidity,
        'condition': forecast.condition,
        'wind_speed': forecast.wind_speed
    }
    return jsonify(result)


@weather_bp.route('/city/<string:city_name>', methods=['GET'])
@swag_from('../docs/weather_swagger/get_forecasts_by_city.yml')
def get_forecasts_by_city(city_name):
    city = City.query.filter_by(name=city_name).first()
    if not city:
        return jsonify({'error': 'City not found.'}), 404

    forecasts = Forecast.query.filter_by(city_id=city.id).all()
    result = [
        {
            'id': forecast.id,
            'city_id': forecast.city_id,
            'date': forecast.date.strftime(DATE_FORMAT),
            'temperature': forecast.temperature,
            'humidity': forecast.humidity,
            'condition': forecast.condition,
            'wind_speed': forecast.wind_speed
        } for forecast in forecasts
    ]
    return jsonify({'forecasts': result})


@weather_bp.route('/<int:forecast_id>', methods=['PUT'])
@swag_from('../docs/weather_swagger/update_forecast.yml')
def update_forecast(forecast_id):
    data = request.json
    forecast = Forecast.query.get_or_404(forecast_id)

    forecast.temperature = data.get('temperature', forecast.temperature)
    forecast.humidity = data.get('humidity', forecast.humidity)
    forecast.condition = data.get('condition', forecast.condition)
    forecast.wind_speed = data.get('wind_speed', forecast.wind_speed)

    db.session.commit()
    return jsonify({'message': 'Forecast updated successfully!'})


@weather_bp.route('/<int:forecast_id>', methods=['DELETE'])
@swag_from('../docs/weather_swagger/delete_forecast.yml')
def delete_forecast(forecast_id):
    forecast = Forecast.query.get_or_404(forecast_id)
    db.session.delete(forecast)
    db.session.commit()
    return jsonify({'message': 'Forecast deleted successfully!'})
