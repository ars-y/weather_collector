from pydantic import HttpUrl, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):

    DATABASE_URL: PostgresDsn

    WEATHER_API_URL: HttpUrl

    WEATHER_API_KEY: str

    RETRY_TIME: int = 60*60

    COOKIE_MAX_AGE: int = 60*30

    JWT_SECRET: str

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )


settings = BaseConfig()
