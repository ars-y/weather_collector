from fastapi import APIRouter

from src.api.v1.schemas.response.user import UserResponseSchema
from src.dependencies.auth import UserDeps


router = APIRouter(prefix='/users', tags=['User'])


@router.get('/me', response_model=UserResponseSchema)
async def read_user(user: UserDeps):
    """
    Returns information about the current user.

    Requireds:
        - authentication.
    """
    return user.to_pydantic_schema()
