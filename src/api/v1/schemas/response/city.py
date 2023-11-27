from datetime import datetime

from pydantic import BaseModel


class CityResponseSchema(BaseModel):

    id: int
    name: str
    country: str
    latitude: float
    longitude: float
    created_at: datetime
    updated_at: datetime
