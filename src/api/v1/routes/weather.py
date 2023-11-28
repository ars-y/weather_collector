from fastapi import APIRouter

from src.api.v1.schemas.response.weather import WeatherResponseSchema
from src.dependencies.common import QueryParamDeps
from src.dependencies.unit_of_work import UOWDep
from src.models.weather import Weather
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


@router.get('/{city_id}')
async def get_current_city_weather(city_id: int, uow: UOWDep):
    pass
