from typing import Annotated

from fastapi import Depends

from src.core.constants import MIN_TEMP, MAX_TEMP


async def get_weather_filters(
    name: str = '',
    description: str = '',
    min_temp: float = MIN_TEMP,
    max_temp: float = MAX_TEMP
) -> dict:
    """
    Gets weather filters.

    Args:
        - `name`: weather name;
        - `description`: weather description;
        - `min_temp` and `max_temp` values
        to filter temperature within a specified range.
    """
    filters: dict = {}
    if name:
        filters.update(name=name)

    if description:
        filters.update(description=description)

    if min_temp or max_temp:
        filters.update(
            min_temp=min_temp,
            max_temp=max_temp,
            temperature=0.0
        )

    return filters


WeatherFiltersDeps = Annotated[dict, Depends(get_weather_filters)]
