from flask import Blueprint, request, jsonify

from app import db
from app.models.models import City

city_bp = Blueprint('city', __name__)

@city_bp.route('/', methods=['POST'])
def create_city():
    data = request.json
    city_name = data.get('name')
    country_name = data.get('country')

    if not city_name:
        return jsonify({'error': 'City name is required.'}), 400
    if not country_name:
        return jsonify({'error': 'Country name is required.'}), 400

    if City.query.filter_by(name=city_name).first():
        return jsonify({'error': f'City {city_name} already exists.'}), 400

    new_city = City(name=city_name, country=country_name)
    db.session.add(new_city)
    db.session.commit()

    return jsonify({'message': f'City {city_name} created successfully!',
                    'city': {'id': new_city.id,
                             'name': new_city.name}
                    }), 201

@city_bp.route('/', methods=['GET'])
def get_all_cities():
    cities = City.query.all()
    result = [{'id': city.id, 'name': city.name, 'country': city.country} for city in cities]
    return jsonify({'cities': result})

@city_bp.route('/<string:city_name>', methods=['GET'])
def get_city_by_name(city_name):
    city = City.query.filter_by(name=city_name).first()
    if not city:
        return jsonify({'error': f'City {city_name} is not found.'}), 404

    result = {'id': city.id, 'name': city.name, 'country': city.country}
    return jsonify(result)

@city_bp.route('/<int:city_id>', methods=['PUT'])
def update_city(city_id):
    data = request.json
    city = City.query.get_or_404(city_id)

    city_name = data.get('name')
    if city_name:
        if City.query.filter_by(name=city_name).first():
            return jsonify({'error': 'City name already exists.'}), 400
        city.name = city_name

    db.session.commit()
    return jsonify({'message': 'City updated successfully!', 'city': {'id': city.id, 'name': city.name}})

@city_bp.route('/<int:city_id>', methods=['DELETE'])
def delete_city(city_id):
    city = City.query.get_or_404(city_id)
    db.session.delete(city)
    db.session.commit()
    return jsonify({'message': f'City {city.name} is deleted successfully!'})
