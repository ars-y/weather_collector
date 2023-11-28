from fastapi import APIRouter, status

from src.api.v1.schemas.request.city import CityCreateSchema
from src.api.v1.schemas.response.city import CityResponseSchema
from src.dependencies.auth import UserDeps
from src.dependencies.common import QueryParamDeps
from src.dependencies.unit_of_work import UOWDep
from src.exceptions.base import PermissionDenied
from src.exceptions.db import ObjectNotFound
from src.models.city import City
from src.services.city import CityService


router = APIRouter(prefix='/city', tags=['City'])


@router.get('', response_model=list[CityResponseSchema])
async def get_cities(
    uow: UOWDep,
    query_params: QueryParamDeps
):
    """
    Receives a list of all available cities.

    Optional query parameters:
        - `offset`: number of skip;
        - `limit`: limit the number of results;
        - `sort_by`: sort by field name;
        - `sort`: ascending or descending.
    """
    cities: list[City] = await CityService.get_all(uow, query_params)
    return [
        city.to_pydantic_schema()
        for city in cities
    ]


@router.get(
    '/{city_id}',
    response_model=CityResponseSchema
)
async def get_current_city(city_id: int, uow: UOWDep):
    """
    Retrieves data for a specific city.

    Args:
        - `city_id` -- city ID.
    """
    city: City = await CityService.get(uow, city_id)
    if not city:
        extra_msg: dict = {
            'reason': 'Object Not Found',
            'description': 'The specified city doesn\'t exist'
        }
        raise ObjectNotFound(extra_msg=extra_msg)

    return city.to_pydantic_schema()


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    response_model=CityResponseSchema
)
async def add_city(city_schema: CityCreateSchema, uow: UOWDep, user: UserDeps):
    """
    Adds a city to the database.

    Args:
        - `city_schema` -- data to create new city;
        - authentication and permissions to create city.
    """
    if not user.is_superuser:
        extra_msg: dict = {
            'reason': 'Permission denied',
            'description': 'No permission to create new object'
        }
        raise PermissionDenied(extra_msg=extra_msg)

    city: City = await CityService.create(uow, city_schema.model_dump())
    return city.to_pydantic_schema()


@router.delete('/{city_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_city(city_id: int, uow: UOWDep, user: UserDeps):
    """
    Removes a city from the database.

    Args:
        - `city_id` -- city ID;
        - authentication and permissions to delete city.
    """
    if not user.is_superuser:
        extra_msg: dict = {
            'reason': 'Permission denied',
            'description': 'No permission to delete object'
        }
        raise PermissionDenied(extra_msg=extra_msg)

    city: City = await CityService.get(uow, city_id)
    if not city:
        extra_msg: dict = {
            'reason': 'Object Not Found',
            'description': 'The specified city doesn\'t exist'
        }
        raise ObjectNotFound(extra_msg=extra_msg)

    await CityService.delete(uow, city.id)
