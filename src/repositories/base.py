from abc import ABC, abstractmethod
from typing import TypeVar, Optional

from sqlalchemy import (
    delete as sql_delete,
    select,
    update as sql_update
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.constants import CITIES_NUMBER
from src.enums.sql import OrderEnum
from src.models.base import Base


SQLModelType = TypeVar('SQLModelType', bound=Base)


class AbstractBaseRepository(ABC):

    _model = None

    @abstractmethod
    async def get(self, pk: int):
        """Returns an object from the database by ID."""
        raise NotImplementedError

    @abstractmethod
    async def get_all(
        self,
        filters: Optional[None] = None,
        offset: int = 0,
        limit: int = CITIES_NUMBER,
        order_by_field: Optional[str] = None,
        order: OrderEnum = OrderEnum.ASCENDING
    ):
        """
        Returns a list of objects from the database.

        Args:
            Optional:
            - `filters`: dict of the form
            {field_name: field_value} to filter by;
            - `offset`: number of skip rows;
            - `limit`: number of rows;
            - `order_by_field`: order by field;
            - `order`: ascending or descending.
        """
        raise NotImplementedError

    @abstractmethod
    async def create(self, data: dict):
        """Creates a new object in the database."""
        raise NotImplementedError

    @abstractmethod
    async def update(self, pk: int, data: dict):
        """
        Updates an object in the database by ID.

        Args:
            - `pk`: object ID;
            - `data`: dict with data to update.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, pk: int):
        """Delete an object from the database by ID."""
        raise NotImplementedError


class SQLAlchemyRepository(AbstractBaseRepository):

    _model: type[SQLModelType]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, pk: int) -> Optional[SQLModelType]:
        stmt = select(self._model).where(self._model.id == pk)
        response = await self._session.execute(stmt)

        return response.scalar_one_or_none()

    async def get_all(
        self,
        filters: Optional[dict] = None,
        offset: int = 0,
        limit: int = CITIES_NUMBER,
        order_by_field: Optional[str] = None,
        order: OrderEnum = OrderEnum.ASCENDING
    ) -> list[SQLModelType]:
        stmt = select(self._model)
        if filters:
            stmt = stmt.filter_by(**filters)

        stmt = stmt.offset(offset).limit(limit)

        columns = self._model.__table__.columns
        if not order_by_field or order_by_field not in columns:
            order_by_field = self._model.id
        else:
            order_by_field = getattr(self._model, order_by_field)

        if order == OrderEnum.ASCENDING:
            stmt = stmt.order_by(order_by_field.asc())
        else:
            stmt = stmt.order_by(order_by_field.desc())

        response = await self._session.execute(stmt)

        return response.scalars().all()

    async def create(self, data: dict) -> SQLModelType:
        db_obj = self._model(**data)
        self._session.add(db_obj)

        return db_obj

    async def update(self, pk: int, data: dict) -> SQLModelType:
        stmt = sql_update(self._model)
        stmt = stmt.where(self._model.id == pk)
        stmt = stmt.values(**data).returning(self._model)
        response = await self._session.execute(stmt)
        obj: Optional[SQLModelType] = response.scalar_one_or_none()

        return obj

    async def delete(self, pk: int) -> SQLModelType:
        stmt = sql_delete(self._model)
        stmt = stmt.where(self._model.id == pk)
        stmt = stmt.returning(self._model)
        response = await self._session.execute(stmt)
        obj: Optional[SQLModelType] = response.scalar_one_or_none()

        return obj
