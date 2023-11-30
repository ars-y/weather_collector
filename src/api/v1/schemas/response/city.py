from datetime import datetime

from pydantic import BaseModel

from src.api.v1.schemas.response.weather import WeatherResponseSchema


class CityResponseSchema(BaseModel):

    id: int
    name: str
    country: str
    latitude: float
    longitude: float
    created_at: datetime
    updated_at: datetime


class CityWithWeatherResponseSchema(CityResponseSchema):

    weather: list[WeatherResponseSchema]
