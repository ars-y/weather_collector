from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, mapped_column

from src.api.v1.schemas.response.user import UserResponseSchema
from src.models.base import Base


class User(SQLAlchemyBaseUserTable[int], Base):

    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_verified: Mapped[bool] = mapped_column(default=False)

    def to_pydantic_schema(self) -> UserResponseSchema:
        return UserResponseSchema(
            id=self.id,
            username=self.username,
            email=self.email,
            is_active=self.is_active,
            is_superuser=self.is_superuser,
            is_verified=self.is_verified,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
