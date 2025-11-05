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

class StripeSettings(BaseSettings):
    STRIPE_PUBLIC_KEY: str
    STRIPE_SECRET_KEY: str
    STRIPE_WEBHOOK_SECRET: str

class Settings(CommonSettings, DatabaseSettings, JwtSettings, StripeSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings() # pyright: ignore[reportCallIssue]