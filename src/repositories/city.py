from src.models.city import City
from src.repositories.base import SQLAlchemyRepository


class CityRepository(SQLAlchemyRepository):

    _model = City
