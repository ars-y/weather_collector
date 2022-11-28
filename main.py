import logging
import time

from collector.conf import WEATHER_API_URL, WEATHER_API_KEY, RETRY_TIME
from collector.types.weather.weather_collector import WeatherCollector
from collector.db.load_cities import load_cities


def main():
    load_cities()
    collector = WeatherCollector()
    while True:
        try:
            coords = collector.get_coords()
            weather = collector.get_data(coords, WEATHER_API_URL, WEATHER_API_KEY)
            collector.save_data(weather)
        except Exception as ex:
            logging.critical(ex)
        finally:
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] : [%(levelname)s] : %(message)s'
    )
    main()
