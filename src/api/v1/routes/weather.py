from fastapi import APIRouter

from src.api.v1.schemas.response.weather import WeatherResponseSchema
from src.dependencies.unit_of_work import UOWDep
from src.models.weather import Weather
from src.services.weather import WeatherService


router = APIRouter(prefix='/weather', tags=['Weather'])


@router.get('', response_model=list[WeatherResponseSchema])
async def get_weather(uow: UOWDep):
    weather_list: list[Weather] = await WeatherService.get_all(uow)
    return [
        weather.to_pydantic_schema()
        for weather in weather_list
    ]
