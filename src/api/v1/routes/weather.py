from fastapi import APIRouter

from src.api.v1.dependencies.filters import WeatherFiltersDeps
from src.api.v1.schemas.response.city import CityWithWeatherResponseSchema
from src.api.v1.schemas.response.weather import WeatherResponseSchema
from src.dependencies.common import QueryParamDeps
from src.dependencies.unit_of_work import UOWDep
from src.exceptions.db import ObjectNotFound
from src.models.city import City
from src.models.weather import Weather
from src.services.city import CityService
from src.services.weather import WeatherService


router = APIRouter(prefix='/weather', tags=['Weather'])


@router.get('', response_model=list[WeatherResponseSchema])
async def get_weather(uow: UOWDep, query_params: QueryParamDeps):
    """
    Get all weather data for available cities.

    Optional query parameters:
        - `offset`: number of skip;
        - `limit`: limit the number of results;
        - `sort_by`: sort by field name;
        - `sort`: ascending or descending.
    """
    weather_list: list[Weather] = await WeatherService.get_all(
        uow,
        query_params
    )
    return [
        weather.to_pydantic_schema()
        for weather in weather_list
    ]


@router.get('/{city_id}', response_model=CityWithWeatherResponseSchema)
async def get_current_city_weather(
    city_id: int,
    uow: UOWDep,
    filters: WeatherFiltersDeps,
    query_params: QueryParamDeps
):
    """
    Get weather data for current city.

    Args:
        - `city_id`: city ID;

    Optional:
        - filters:
            - `name`: weather name;
            - `description`: weather description;
            - `min_temp` and `max_temp` values
            to filter temperature within a specified range.

        - query parameters:
            - `offset`: number of skip;
            - `limit`: limit the number of results;
            - `sort_by`: sort by field name;
            - `sort`: ascending or descending.
    """
    records: list[tuple[City, Weather]] = (
        await CityService.get_city_with_weather(
            uow,
            city_id,
            filters,
            **query_params
        )
    )

    if not records:
        extra_msg: dict = {
            'reason': 'Object Not Found',
            'description': 'There are no records with the specified parameters'
        }
        raise ObjectNotFound(extra_msg=extra_msg)

    city: City = records[0][0]

    return CityWithWeatherResponseSchema(
        **city.to_pydantic_schema().model_dump(),
        weather=[
            weather.to_pydantic_schema()
            for _, weather in records
        ]
    )
