from flask import Blueprint, request, jsonify
from flasgger import swag_from

from app import db
from app.models.models import City
from app.utils import get_city_coordinates, populate_db_with_forecasts

city_bp = Blueprint('city', __name__)

@city_bp.route('/', methods=['POST'])
@swag_from('../docs/city_swagger/create_city.yml')
def create_city():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must be JSON.'}), 400

    city_name = data.get('name')
    country_name = data.get('country')

    if not city_name:
        return jsonify({'error': 'City name is required.'}), 400
    if not country_name:
        return jsonify({'error': 'Country name is required.'}), 400

    if City.query.filter_by(name=city_name).first():
        return jsonify({'error': f'City {city_name} already exists.'}), 400

    latitude, longitude = get_city_coordinates(city_name)
    if not (latitude and longitude):
        return jsonify({'error': f'Could not get city coordinates. Is {city_name} a valid city name?'}), 400

    new_city = City(name=city_name, country=country_name, latitude=latitude, longitude=longitude)
    db.session.add(new_city)
    db.session.commit()
    populate_db_with_forecasts()

    return jsonify({'message': f'City {city_name} created successfully!',
                    'city': {'id': new_city.id,
                             'name': new_city.name,
                             'country': new_city.country,
                             'latitude': new_city.latitude,
                             'longitude': new_city.longitude}
                    }), 201


@city_bp.route('/', methods=['GET'])
@swag_from('../docs/city_swagger/get_cities.yml')
def get_cities():
    city_name = request.args.get('name')
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')

    if city_name or (latitude and longitude):
        if city_name:
            city = City.query.filter_by(name=city_name).first()
            if not city:
                return jsonify({'error': f'City {city_name} not found.'}), 404
        else:
            try:
                latitude_val = float(latitude)
                longitude_val = float(longitude)
            except ValueError:
                return jsonify({'error': 'Invalid latitude or longitude values.'}), 400

            city = City.query.filter_by(latitude=latitude_val, longitude=longitude_val).first()
            if not city:
                return jsonify({'error': f'City with coordinates ({latitude_val}, {longitude_val}) not found.'}), 404

        result = {
            'id': city.id,
            'name': city.name,
            'latitude': city.latitude,
            'longitude': city.longitude,
            'country': city.country
        }
        return jsonify(result)
    else:
        cities = City.query.all()
        result = [{
            'id': city.id,
            'name': city.name,
            'latitude': city.latitude,
            'longitude': city.longitude,
            'country': city.country
        } for city in cities]
        return jsonify({'cities': result})

@city_bp.route('/<int:city_id>', methods=['PUT'])
@swag_from('../docs/city_swagger/update_city.yml')
def update_city(city_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must be JSON.'}), 400

    city = City.query.get_or_404(city_id)

    new_name = data.get('name')
    if new_name:
        existing_city = City.query.filter_by(name=new_name).first()
        if existing_city and existing_city.id != city_id:
            return jsonify({'error': 'City name already exists.'}), 400
        city.name = new_name
    else:
        new_name = city.name

    new_country = data.get('country')
    if new_country:
        city.country = new_country

    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if latitude is not None or longitude is not None:
        if latitude is None or longitude is None:
            return jsonify({'error': 'Both latitude and longitude must be provided.'}), 400
        try:
            city.latitude = float(latitude)
            city.longitude = float(longitude)
        except ValueError:
            return jsonify({'error': 'Invalid latitude or longitude values.'}), 400
    elif new_name:
        new_lat, new_lon = get_city_coordinates(new_name)
        if not (new_lat and new_lon):
            return jsonify({'error': f'Could not get city coordinates, is {new_name} a valid city name?'}), 400
        city.latitude = new_lat
        city.longitude = new_lon

    db.session.commit()

    return jsonify({
        'message': 'City updated successfully!',
        'city': {
            'id': city.id,
            'name': city.name,
            'country': city.country,
            'latitude': city.latitude,
            'longitude': city.longitude
        }
    })


@city_bp.route('/<int:city_id>', methods=['DELETE'])
@swag_from('../docs/city_swagger/delete_city.yml')
def delete_city(city_id):
    city = City.query.get_or_404(city_id)
    db.session.delete(city)
    db.session.commit()
    return jsonify({'message': f'City {city.name} is deleted successfully!'})
