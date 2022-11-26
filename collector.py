import logging
import requests
from conf import engine
from sqlalchemy.orm import sessionmaker
from models import City, Weather

Session = sessionmaker(bind=engine)
session = Session()

class Collector:
    """Коллектор собирает данные о погоде и сохраняет в бд."""
    def __init__(self) -> None:
        pass

    def get_coords(self) -> list:
        """Возвращает широту и долготу."""
        coordinates: list[tuple] = [
            (latitude, longitude)
            for latitude, longitude in session.query(City.latitude, City.longitude)
        ]
        if len(coordinates) == 0:
            raise Exception('Coordinates is empty.')
        logging.debug('Coordinates is received.')
        return coordinates

    def get_weather(self, coordinates: list[tuple], url: str, key: str) -> list:
        """Получить погоду."""
        data: list = []
        for coords in coordinates:
            latitude, longitude = coords
            params: dict = {
                'lat': latitude, 'lon': longitude,
                'units': 'metric', 'APPID': key
            }
            logging.debug('GET requiest to weather API.')
            response = requests.get(url, params)
            if response.status_code != 200:
                raise Exception(f'Response status code: {response.status_code}')
            data.append(response.json())
        if len(data) == 0:
            raise Exception('Weather data is empty.')
        logging.debug('Weather data is received.')
        return data
    
    def save(self, data: list) -> None:
        """Сохранить погоду."""
        logging.debug('Start saving data.')
        for id, row in enumerate(data, start=1):
            city = session.query(City).get(id)
            weather = Weather(
                city=city,
                weather_type=row.get('weather')[0].get('main'),
                description=row.get('weather')[0].get('description'),
                temperature=row.get('main').get('temp'),
                min_temp=row.get('main').get('temp_min'),
                max_temp=row.get('main').get('temp_max'),
            )
            session.add(weather)
        session.commit()
        logging.debug('Saving data is succesfully.')
