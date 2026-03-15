from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Fast-API"
    DEBUG: bool = False
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    RESERVATION_MIN_HOURS: int = 1

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
