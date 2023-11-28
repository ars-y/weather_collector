from fastapi_users import schemas


class UserCreateSchema(schemas.BaseUserCreate):

    username: str
