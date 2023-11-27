from datetime import datetime

from pydantic import BaseModel


class WeatherResponseSchema(BaseModel):

    id: int
    name: str
    description: str
    temperature: float
    min_temp: float
    max_temp: float
    humidity: int
    wind_speed: float
    created_at: datetime
    updated_at: datetime
