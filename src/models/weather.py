from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.v1.schemas.response.weather import WeatherResponseSchema
from src.models.base import Base

if TYPE_CHECKING:
    from src.models.city import City


class Weather(Base):

    __tablename__ = 'weather'

    name: Mapped[str]
    description: Mapped[str]
    temperature: Mapped[float]
    min_temp: Mapped[float]
    max_temp: Mapped[float]
    humidity: Mapped[int]
    wind_speed: Mapped[float]
    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))

    city: Mapped['City'] = relationship(
        back_populates='weather'
    )

    def to_pydantic_schema(self) -> WeatherResponseSchema:
        return WeatherResponseSchema(
            id=self.id,
            name=self.name,
            description=self.description,
            temperature=self.temperature,
            min_temp=self.min_temp,
            max_temp=self.max_temp,
            humidity=self.humidity,
            wind_speed=self.wind_speed,
            city_id=self.city_id,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
