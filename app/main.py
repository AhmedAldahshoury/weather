import os

from flask import Flask
from flasgger import Swagger
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from routes import weather_routes

app = Flask(__name__)
app.register_blueprint(weather_routes, url_prefix='/weather')
swagger = Swagger(app)
load_dotenv()


app.config['SWAGGER'] = {
    'title': 'Weather API',
    'uiversion': 3
}
SA_PASSWORD = os.getenv("SA_PASSWORD")
if not SA_PASSWORD:
    raise ValueError("SA_PASSWORD is not set in .env file.")

app.config["SQLALCHEMY_DATABASE_URI"] = f"mssql+pyodbc://sa:{SA_PASSWORD}@mssql_container:1433/WeatherDB?driver=ODBC+Driver+17+for+SQL+Server"

db = SQLAlchemy(app)
migrate = Migrate(app, db)
if __name__ == '__main__':
    app.run(debug=True)
