from flask import Flask

from app.constants import CITIES_LIST
from app.utils import populate_db_with_cities, populate_forecasts


def register_commands(app: Flask):
    @app.cli.command("populate-db")
    def populate_db():
        populate_db_with_cities(CITIES_LIST)
        populate_forecasts()