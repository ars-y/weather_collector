from fastapi import APIRouter

from src.api.v1.schemas.request.user import UserCreateSchema
from src.api.v1.schemas.response.user import UserResponseSchema
from src.core.auth import auth_backend
from src.dependencies.auth import fastapi_users


auth_router = fastapi_users.get_auth_router(auth_backend)

register_router = fastapi_users.get_register_router(
    UserResponseSchema,
    UserCreateSchema
)


routers: list[APIRouter] = [
    auth_router,
    register_router,
]
