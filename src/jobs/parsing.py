import asyncio
import json

import aiohttp
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.conf import settings
from src.dependencies.unit_of_work import get_uow
from src.exceptions.base import BadRequest
from src.models.city import City
from src.services.city import CityService
from src.services.weather import WeatherService


async def get_cities(uow: AsyncSession) -> list[City]:
    """Returns list of all cities from database."""
    return await CityService.get_all(uow)


async def preparing_request_params(cities: list[City]) -> list[dict]:
    """
    Preparing a dict with query parameters.
    Additionally, the `city_id` is included
    for further connection with the weather table.
    """
    return [
        {
            'lat': city.latitude,
            'lon': city.longitude,
            'appid': settings.WEATHER_API_KEY,
            'city_id': city.id,
        }
        for city in cities
    ]


async def task_executor(url: str, query_params: list) -> list[dict]:
    """
    Async executing requests to the weather API
    with query parameters for each city.
    ---
    Args:
        - `url` -- weather API URL;
        - `query_params` -- list of query parameters for one city.
    ---
    Return:
        - list with weather data to save it.
    """
    async with aiohttp.ClientSession() as session:
        tasks: list = [
            request_weather_data(session, url, params)
            for params in query_params
        ]
        return await asyncio.gather(*tasks)


async def request_weather_data(
    session: aiohttp.ClientSession,
    url: str,
    params: dict
) -> dict:
    """
    Making async request to weather API to get weather data.
    ---
    Args:
        - `session` -- client session for make HTTP request;
        - `url` -- weather API URL;
        - `params` -- query parameters.
    ---
    Return:
        - dict with weather data and `city_id` to bound it with City table.
    """
    city_id: int = params.pop('city_id')
    async with session.get(url, params=params) as response:
        if response.status != status.HTTP_200_OK:
            extra_msg: dict = {
                'reason': 'Bad Request',
                'description': 'Failed to get data from openweather API',
                'detail': {
                    'city_id': city_id
                }
            }
            raise BadRequest(extra_msg=extra_msg)

        data_bytes: bytes = await response.read()
        data: dict = json.loads(data_bytes.decode())
        data.update(city_id=city_id)

        return data


async def save_weather_data(uow: AsyncSession, data: dict) -> None:
    """Saving weather data in database."""
    weather_data: dict = data.get('weather')[0]
    temp_data: dict = data.get('main')

    weather_create_data: dict = {
        'name': weather_data.get('main'),
        'description': weather_data.get('description'),
        'temperature': temp_data.get('temp'),
        'min_temp': temp_data.get('temp_min'),
        'max_temp': temp_data.get('temp_max'),
        'humidity': temp_data.get('humidity'),
        'wind_speed': data.get('wind').get('speed'),
        'city_id': data.get('city_id')
    }
    await WeatherService.create(uow, weather_create_data)


async def main() -> None:
    """Receiving weather data and then storing it in the database."""
    uow: AsyncSession = next(get_uow())
    url: str = str(settings.WEATHER_API_URL)

    cities: list[City] = await get_cities(uow)
    query_params: list[dict] = await preparing_request_params(cities)
    weather_data: list[dict] = await task_executor(url, query_params)

    for data in weather_data:
        await save_weather_data(uow, data)


if __name__ == '__main__':
    asyncio.run(main())
