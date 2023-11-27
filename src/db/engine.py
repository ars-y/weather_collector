from sqlalchemy.ext.asyncio import create_async_engine

from src.core.conf import settings


engine = create_async_engine(str(settings.DATABASE_URL))
