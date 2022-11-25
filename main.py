import logging
from conf import WEATHER_API_URL, WEATHER_API_KEY
from collector import Collector
from load_cities import load_cities


def main():
    load_cities()
    collector = Collector()
    coordinates = collector.get_coords()
    data = collector.get_weather(coordinates, WEATHER_API_URL, WEATHER_API_KEY)
    collector.save(data)

    from conf import engine
    from sqlalchemy.orm import sessionmaker
    from models import Weather

    Session = sessionmaker(bind=engine)
    session = Session()

    for instance in session.query(Weather).all():
        print(instance)
    

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] : [%(levelname)s] : %(message)s'
    )
    main()
