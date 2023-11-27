from contextlib import asynccontextmanager
from typing import Generator

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

from src.api.v1.routers import api_v1_router
from src.core.conf import settings
from src.core.constants import DESCRIPTION_APP, TITLE_APP
from src.jobs import parsing


@asynccontextmanager
async def lifespan(app: FastAPI) -> Generator:
    """Lifespan for job scheduler."""
    schedulers = AsyncIOScheduler()
    schedulers.add_job(
        parsing.main,
        'interval',
        seconds=settings.RETRY_TIME
    )
    schedulers.start()

    yield

    schedulers.shutdown()


def create_app() -> FastAPI:
    app = FastAPI(
        title=TITLE_APP,
        description=DESCRIPTION_APP,
        lifespan=lifespan
    )

    app.include_router(api_v1_router)

    return app


app = create_app()
