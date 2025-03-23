from flask import Blueprint, request, jsonify
from flasgger import swag_from

from app import db
from app.models.models import City
from app.utils import get_city_coordinates

city_bp = Blueprint('city', __name__)

@city_bp.route('/', methods=['POST'])
@swag_from('../docs/city_swagger/create_city.yml')
def create_city():
    data = request.json
    city_name = data.get('name')
    country_name = data.get('country')
    if not city_name:
        return jsonify({'error': 'City name is required.'}), 400

    latitude, longitude = get_city_coordinates(city_name)

    if not (latitude and longitude):
        return jsonify({'error': f'Could not get city coordinates, is {city_name} a valid city name?.'}), 400

    if not country_name:
        return jsonify({'error': 'Country name is required.'}), 400

    if City.query.filter_by(name=city_name).first():
        return jsonify({'error': f'City {city_name} already exists.'}), 400


    new_city = City(name=city_name, country=country_name, latitude=latitude, longitude=longitude)
    db.session.add(new_city)
    db.session.commit()

    return jsonify({'message': f'City {city_name} created successfully!',
                    'city': {'id': new_city.id,
                             'name': new_city.name,
                             'latitude': new_city.latitude,
                             'longitude': new_city.longitude}
                    }), 201

@city_bp.route('/', methods=['GET'])
@swag_from('../docs/city_swagger/get_all_cities.yml')
def get_all_cities():
    cities = City.query.all()
    result = [{'id': city.id,
               'name': city.name,
               'latitude': city.latitude,
               'longitude': city.longitude,
               'country': city.country
               } for city in cities]
    return jsonify({'cities': result})

@city_bp.route('/<string:city_name>', methods=['GET'])
@swag_from('../docs/city_swagger/get_city_by_name.yml')
def get_city_by_name(city_name):
    city = City.query.filter_by(name=city_name).first()
    if not city:
        return jsonify({'error': f'City {city_name} is not found.'}), 404

    result = {'id': city.id,
              'name': city.name,
              'latitude': city.latitude,
              'longitude': city.longitude,
              'country': city.country}
    return jsonify(result)

@city_bp.route('/', methods=['GET'])
@swag_from('../docs/city_swagger/get_city_by_coordinates.yml')
def get_city_by_coordinates():
    try:
        city_latitude = float(request.args.get('latitude'))
        city_longitude = float(request.args.get('longitude'))
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid or missing latitude and longitude query parameters.'}), 400

    city = City.query.filter_by(latitude=city_latitude, longitude=city_longitude).first()
    if not city:
        return jsonify({'error': f'City with coordinates {city_latitude, city_longitude} is not found.'}), 404

    result = {'id': city.id,
              'name': city.name,
              'latitude': city.latitude,
              'longitude': city.longitude,
              'country': city.country}
    return jsonify(result)


@city_bp.route('/<int:city_id>', methods=['PUT'])
@swag_from('../docs/city_swagger/update_city.yml')
def update_city(city_id):
    data = request.json
    city = City.query.get_or_404(city_id)

    city_name = data.get('name')
    country = data.get('country')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if city_name:
        existing_city = City.query.filter_by(name=city_name).first()
        if existing_city and existing_city.id != city_id:
            return jsonify({'error': 'City name already exists.'}), 400
        city.name = city_name

    if country:
        city.country = country

    if not any([latitude, longitude]):
        latitude, longitude = get_city_coordinates(city_name)
        if not any([latitude, longitude]):
            return jsonify({'error': f'Could not get city coordinates, is {city_name} a valid city name?.'}), 400

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
