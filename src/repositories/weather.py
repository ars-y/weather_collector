from src.models.weather import Weather
from src.repositories.base import SQLAlchemyRepository


class WeatherRepository(SQLAlchemyRepository):

    _model = Weather
