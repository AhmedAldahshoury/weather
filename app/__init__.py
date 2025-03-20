from flask import Flask
from routes import weather_routes
app = Flask(__name__)
app.register_blueprint(weather_routes, url_prefix='/weather')

if __name__ == '__main__':
    app.run(debug=True)
