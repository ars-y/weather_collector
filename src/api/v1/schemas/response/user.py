from datetime import datetime

from fastapi_users import schemas


class UserResponseSchema(schemas.BaseUser[int]):

    username: str
    created_at: datetime
    updated_at: datetime
