from pydantic import BaseSettings

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
