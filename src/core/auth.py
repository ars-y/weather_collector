from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy
)

from src.core.conf import settings


cookie_transport = CookieTransport(cookie_max_age=settings.COOKIE_MAX_AGE)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        settings.JWT_SECRET,
        settings.COOKIE_MAX_AGE
    )


auth_backend = AuthenticationBackend(
    'jwt',
    cookie_transport,
    get_jwt_strategy
)
