import logging
import os

from flask import Flask, jsonify
from flasgger import Swagger
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from routes import weather_routes

app = Flask(__name__)
swagger = Swagger(app)
load_dotenv()

app.config['SWAGGER'] = {
    'title': 'Weather API',
    'uiversion': 3
}
SA_PASSWORD = os.getenv("SA_PASSWORD")
if not SA_PASSWORD:
    raise ValueError("SA_PASSWORD is not set in .env file.")

app.config["SQLALCHEMY_DATABASE_URI"] = f"mssql+pyodbc://sa:{SA_PASSWORD}@mssql_container:1433/master?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=Yes&Encrypt=No"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.register_blueprint(weather_routes, url_prefix='/weather')


@app.route('/test_connection', methods=['GET'])
def test_connection():
    try:
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            return jsonify({"message": "Database connection successful"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
