import logging
from csv import DictReader
from conf import engine
from sqlalchemy.orm import sessionmaker
from models import City

Session = sessionmaker(bind=engine)
session = Session()

filename = 'fifty_biggest_cities_by_population.csv'

def load_cities():
    query = session.query(City).all()
    if len(query) != 0:
        logging.info(f'{filename} is already loaded.')
        return

    for row in DictReader(open(f'./data/{filename}')):
        city = City(
            city_name=row.get('city'),
            country=row.get('country'),
            latitude=row.get('latitude'),
            longitude=row.get('longitude')
        )
        session.add(city)
    session.commit()
