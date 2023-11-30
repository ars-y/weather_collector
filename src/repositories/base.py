from abc import ABC, abstractmethod
from typing import TypeVar

from sqlalchemy import (
    Select,
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
        filters: dict | None = None,
        offset: int = 0,
        limit: int = CITIES_NUMBER,
        order_by_field: str | None = None,
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

    async def get(self, pk: int) -> SQLModelType | None:
        stmt = select(self._model).where(self._model.id == pk)
        response = await self._session.execute(stmt)

        return response.scalar_one_or_none()

    async def get_all(
        self,
        filters: dict | None = None,
        **query_params
    ) -> list[SQLModelType]:
        stmt = select(self._model)
        if filters:
            stmt = stmt.filter_by(**filters)

        if query_params:
            stmt = await self._apply_query_params(stmt, **query_params)

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
        obj: SQLModelType | None = response.scalar_one_or_none()

        return obj

    async def delete(self, pk: int) -> SQLModelType:
        stmt = sql_delete(self._model)
        stmt = stmt.where(self._model.id == pk)
        stmt = stmt.returning(self._model)
        response = await self._session.execute(stmt)
        obj: SQLModelType | None = response.scalar_one_or_none()

        return obj

    async def _apply_query_params(
        self,
        stmt: Select,
        offset: int = 0,
        limit: int = CITIES_NUMBER,
        order_by_field: str | None = None,
        order: OrderEnum = OrderEnum.ASCENDING,
        *,
        model: SQLModelType | None = None
    ) -> Select:
        """
        Returns statement with applied parameters.

        The `model` keyword allows to select another SQL model
        for which to apply the parameters (JOIN cases).
        """
        if not model:
            model = self._model

        stmt = stmt.offset(offset).limit(limit)

        columns = model.__table__.columns
        if not order_by_field or order_by_field not in columns:
            order_by_field = model.id
        else:
            order_by_field = getattr(model, order_by_field)

        if order == OrderEnum.ASCENDING:
            stmt = stmt.order_by(order_by_field.asc())
        else:
            stmt = stmt.order_by(order_by_field.desc())

        return stmt
