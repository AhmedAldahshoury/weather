from app import db

class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class Weather(db.Model):
    __tablename__ = 'weather'
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    temperature = db.Column(db.String(10), nullable=False)
    humidity = db.Column(db.String(10), nullable=False)
    condition = db.Column(db.String(50), nullable=False)
    wind_speed = db.Column(db.String(10), nullable=False)
