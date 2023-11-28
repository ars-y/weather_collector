from typing import Annotated

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.sessions import get_session
from src.models.user import User


async def get_user_db(
    session: Annotated[AsyncSession, Depends(get_session)]
):
    yield SQLAlchemyUserDatabase(session, User)
