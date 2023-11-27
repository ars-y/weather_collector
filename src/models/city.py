from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from src.api.v1.schemas.response.city import CityResponseSchema
from src.models.base import Base

if TYPE_CHECKING:
    from src.models.weather import Weather


class City(Base):

    __tablename__ = 'city'

    name: Mapped[str]
    country: Mapped[str]
    latitude: Mapped[float]
    longitude: Mapped[float]

    weather: Mapped['Weather'] = relationship(
        back_populates='city'
    )

    def to_pydantic_schema(self) -> CityResponseSchema:
        return CityResponseSchema(
            id=self.id,
            name=self.name,
            country=self.country,
            latitude=self.latitude,
            longitude=self.longitude,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
