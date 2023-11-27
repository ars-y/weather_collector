from pydantic import BaseModel


class WeatherCreateSchema(BaseModel):

    name: str
    description: str
    temperature: float
    min_temp: float
    max_temp: float
    humidity: int
    wind_speed: float
    city_id: int
