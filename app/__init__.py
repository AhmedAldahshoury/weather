import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger
from dotenv import load_dotenv

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    load_dotenv()
    app = Flask(__name__)

    # Load configuration
    SA_PASSWORD = os.getenv("SA_PASSWORD")
    if not SA_PASSWORD:
        raise ValueError("SA_PASSWORD is not set in .env file.")

    app.config['SWAGGER'] = {
        'title': 'Weather API',
        'uiversion': 3
    }
    app.config[
        "SQLALCHEMY_DATABASE_URI"] = f"mssql+pyodbc://sa:{SA_PASSWORD}@mssql_container:1433/master?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=Yes&Encrypt=No"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    from app.routes.weather_routes import weather_routes
    app.register_blueprint(weather_routes, url_prefix='/weather')

    return app
