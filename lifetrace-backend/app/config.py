from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+pymysql://root:root123@mysql:3306/lifetrace"
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    WEATHER_API_KEY: str = ""
    CORS_ORIGINS: List[str] = ["http://localhost:5173"]
    JWT_SECRET_KEY: str = "lifetrace-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24

    class Config:
        env_file = ".env"

settings = Settings()
