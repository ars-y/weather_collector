import os
from sqlalchemy import create_engine

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

engine = create_engine('sqlite:///:memory:', echo=True)


WEATHER_API_URL: str = os.getenv('WEATHER_API_URL')

WEATHER_API_KEY: str = os.getenv('WEATHER_API_KEY')
