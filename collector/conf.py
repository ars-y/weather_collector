import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

url_object = URL.create(
    'postgresql',
    username=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_NAME')
)
engine = create_engine(url_object, echo=True)
engine.connect()


WEATHER_API_URL: str = os.getenv('WEATHER_API_URL')

WEATHER_API_KEY: str = os.getenv('WEATHER_API_KEY')

RETRY_TIME: int = int(os.getenv('RETRY_TIME', 60 * 60))
