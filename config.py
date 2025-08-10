from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    JWT_SECRET_KEY: str
    DATABASE_URL: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALLOWED_ORIGINS: str = "http://localhost,http://localhost:3000"
    PORT: int = 8000
    ENV: str = "production"

    class Config:
        env_file = ".env"

settings = Settings()
