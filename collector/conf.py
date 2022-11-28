import os
from sqlalchemy import create_engine

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

#engine = create_engine('sqlite:///:memory:', echo=True)
engine = create_engine('sqlite:///sqlite.db', echo = True)


WEATHER_API_URL: str = os.getenv('WEATHER_API_URL')

WEATHER_API_KEY: str = os.getenv('WEATHER_API_KEY')

RETRY_TIME: int = int(os.getenv('RETRY_TIME', 60 * 60))
