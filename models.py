from sqlalchemy import (
    Column, Integer, String,
    ForeignKey, DateTime, Float
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from conf import engine

Base = declarative_base()


class City(Base):
    __tablename__ = 'cities_table'
    id = Column(Integer, primary_key=True)
    city_name = Column(String(180))
    country = Column(String(70))
    latitude = Column(Float)
    longitude = Column(Float)
    weather = relationship('Weather', backref='city')

    def __repr__(self) -> str:
        return '<City({}, {}, {}, {})>'.format(self.id, self.city_name, self. country, self.weather)
    


class Weather(Base):
    __tablename__ = 'weather_table'
    id = Column(Integer, primary_key=True)
    weather_type = Column(String(100), nullable=False)
    temperature = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    min_temp = Column(Integer, nullable=False)
    max_temp = Column(Integer, nullable=False)
    created = Column(DateTime(), default=datetime.now)
    weather_id = Column(Integer, ForeignKey('cities_table.id'))

    def __repr__(self) -> str:
        return '<Weather({}, {}, {})>'.format(self.id, self.weather_type, self. weather_id)


Base.metadata.create_all(engine)
