from typing import Annotated

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager,
    IntegerIDMixin,
    exceptions
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from src.api.v1.schemas.request.user import UserCreateSchema
from src.models.user import User
from src.repositories.user import get_user_db


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):

    async def create(
        self,
        user_create: UserCreateSchema,
        safe: bool = False,
        request: Request | None = None
    ) -> User:
        await self.validate_password(user_create.password, user_create)

        existing_user: User | None = await self.user_db.get_by_email(
            user_create.email
        )
        if existing_user:
            raise exceptions.UserAlreadyExists()

        user_dict: dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password: str = user_dict.pop('password')
        user_dict['hashed_password'] = self.password_helper.hash(password)

        created_user: User = await self.user_db.create(user_dict)

        return created_user


async def get_user_manager(
    user_db: Annotated[SQLAlchemyUserDatabase, Depends(get_user_db)]
):
    yield UserManager(user_db)
