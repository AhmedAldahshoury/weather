from flask import Flask
from flasgger import Swagger

from routes import weather_routes

app = Flask(__name__)
app.register_blueprint(weather_routes, url_prefix='/weather')
app.config['SWAGGER'] = {
    'title': 'Weather API',
    'uiversion': 3
}
swagger = Swagger(app)


if __name__ == '__main__':
    app.run(debug=True)
