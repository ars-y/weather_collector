from fastapi import APIRouter

from src.api.v1.routes import weather


api_v1_router = APIRouter(prefix='/api/v1')

v1_routers: list = [
    weather.router,
]

for router in v1_routers:
    api_v1_router.include_router(router)
