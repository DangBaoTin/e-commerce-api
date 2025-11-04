# app/core/config.py
from pydantic_settings import BaseSettings

class CommonSettings(BaseSettings):
    APP_NAME: str = "E-Commerce API"
    DEBUG: bool = False

class DatabaseSettings(BaseSettings):
    DATABASE_URL: str

class JwtSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

class Settings(CommonSettings, DatabaseSettings, JwtSettings):
    """
    Main settings class that aggregates all other settings.
    It automatically reads from environment variables and .env file.
    """
    class Config:
        # This tells pydantic-settings to read from a .env file
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create a single instance that the rest of our app can import
settings = Settings()