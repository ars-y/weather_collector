from fastapi import APIRouter

from src.api.v1.routes import auth, city, weather, users


api_v1_router = APIRouter(prefix='/api/v1')

for router in auth.routers:
    api_v1_router.include_router(router, prefix='/auth', tags=['Auth'])

v1_routers: list = [
    city.router,
    weather.router,
    users.router,
]

for router in v1_routers:
    api_v1_router.include_router(router)
