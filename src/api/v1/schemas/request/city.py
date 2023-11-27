from pydantic import BaseModel


class CityCreateSchema(BaseModel):

    name: str
    country: str
    latitude: float
    longitude: float
