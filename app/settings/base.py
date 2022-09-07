from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    PG_HOST: str
    PG_DATABASE: str
    PG_USER: str
    PG_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"


settings = Settings()

settings.PG_HOST = os.environ.get('PG_HOST')
settings.PG_USER = os.environ.get('PG_USER')
settings.PG_PASSWORD = os.environ.get('PG_PASSWORD')
settings.SECRET_KEY = os.environ.get('SECRET_KEY')
settings.ALGORITHM = os.environ.get('ALGORITHM')
settings.ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get(
    'ACCESS_TOKEN_EXPIRE_MINUTES')
