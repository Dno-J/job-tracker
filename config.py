# config.py

from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # -------------------------------
    # 🌍 Environment & Port Settings
    # -------------------------------
    ENV: str = "development"
    PORT: int = 8000

    # -------------------------------
    # 🗄️ Database Configuration
    # -------------------------------
    DATABASE_URL: str

    # -------------------------------
    # 🔐 JWT Configuration
    # -------------------------------
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # -------------------------------
    # 🌐 CORS Configuration
    # -------------------------------
    ALLOWED_ORIGINS: List[str] = ["http://localhost"]

    # -------------------------------
    # 🧩 Compatibility Aliases
    # -------------------------------
    @property
    def SECRET_KEY(self) -> str:
        return self.JWT_SECRET_KEY

    @property
    def ALGORITHM(self) -> str:
        return self.JWT_ALGORITHM

    # -------------------------------
    # 📦 .env File Loading
    # -------------------------------
    class Config:
        env_file = ".env"
        case_sensitive = True

# Instantiate settings object
settings = Settings()
