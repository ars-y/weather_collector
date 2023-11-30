from sqlalchemy import Select, select

from src.models.city import City
from src.models.weather import Weather
from src.repositories.base import SQLAlchemyRepository


class CityRepository(SQLAlchemyRepository):

    _model = City
    _weather_model = Weather

    async def get_city_with_weather(
        self,
        pk: int,
        filters: dict | None = None,
        **query_params
    ) -> list[tuple[City, Weather]]:
        """
        Returns records about a specified city and its weather

        Args:
            - `pk`: city ID.

            Optional:
            - `filters`: dict of the form
            {field_name: field_value} to filter by;
            - `offset`: number of skip rows;
            - `limit`: number of rows;
            - `order_by_field`: order by field;
            - `order`: ascending or descending.
        """
        stmt = select(self._model, self._weather_model)
        stmt = stmt.join(
            self._weather_model,
            self._weather_model.city_id == self._model.id
        )
        stmt = stmt.filter(self._model.id == pk)

        if filters:
            stmt = await self._apply_weather_filters(stmt, filters)

        if query_params:
            stmt = await self._apply_query_params(
                stmt,
                model=self._weather_model,
                **query_params
            )

        response = await self._session.execute(stmt)
        return response.all()

    async def _apply_weather_filters(
        self,
        stmt: Select,
        filters: dict
    ) -> Select:
        """Returns statement with applied filters."""
        min_temp: float = filters.pop('min_temp')
        max_temp: float = filters.pop('max_temp')

        for field in filters:
            if isinstance(filters[field], str):
                stmt = stmt.filter(
                    getattr(self._weather_model, field)
                    .ilike(f'%{filters[field]}%')
                )
            else:
                stmt = stmt.filter(
                    getattr(self._weather_model, field)
                    .between(min_temp, max_temp)
                )

        return stmt
