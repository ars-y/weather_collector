from typing import Annotated

from fastapi import Depends
from fastapi_users import FastAPIUsers

from src.core.auth import auth_backend
from src.models.user import User
from src.services.user import get_user_manager


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)

current_user = fastapi_users.current_user(active=True)

UserDeps = Annotated[User, Depends(current_user)]
