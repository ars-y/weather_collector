import logging
import time
from conf import WEATHER_API_URL, WEATHER_API_KEY
from collector import Collector
from load_cities import load_cities


def main():
    from conf import engine
    from sqlalchemy.orm import sessionmaker
    from models import Weather, City

    Session = sessionmaker(bind=engine)
    session = Session()

    load_cities()
    collector = Collector()
    while True:
        try:
            coordinates = collector.get_coords()
            data = collector.get_weather(coordinates, WEATHER_API_URL, WEATHER_API_KEY)
            collector.save(data)

            for instance in session.query(Weather).all():
                print(instance)
    
            for city in session.query(City).filter(City.city_name=='Tokyo'):
                print(city)
        except Exception as ex:
            logging.critical(ex)
        finally:
            time.sleep(30 * 1)
    

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] : [%(levelname)s] : %(message)s'
    )
    main()
