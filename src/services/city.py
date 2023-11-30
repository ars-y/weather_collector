from src.models.city import City
from src.models.weather import Weather
from src.services.base import StorageBaseService


class CityService(StorageBaseService):

    _repository = 'city_repository'

    @classmethod
    async def get_city_with_weather(
        cls,
        uow,
        pk: int,
        filters: dict | None = None,
        **query_params
    ) -> list[tuple[City, Weather]]:
        """Returns records about a specified city and its weather."""
        async with uow:
            return (
                await uow.__dict__[cls._repository]
                .get_city_with_weather(pk, filters, **query_params)
            )
