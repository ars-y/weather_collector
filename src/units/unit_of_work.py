from types import TracebackType
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.city import CityRepository
from src.repositories.weather import WeatherRepository
from src.units.base import AbstractBaseUnitOfWork


class UnitOfWork(AbstractBaseUnitOfWork):

    def __init__(self, sessionmaker: Callable[..., AsyncSession]) -> None:
        self._session_factory = sessionmaker

    async def __aenter__(self):
        self._session: AsyncSession = self._session_factory()

        self.city_repository = CityRepository(self._session)
        self.weather_repository = WeatherRepository(self._session)

        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException],
        exc_val: BaseException,
        exc_tb: TracebackType
    ):
        if any((exc_type, exc_val, exc_tb)):
            await self.rollback()
        else:
            await self.commit()

        await self._session.close()

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
