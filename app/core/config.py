from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Pydantic сам посмотрит в .env или в переменные Docker
    # Если не найдет там DATABASE_URL, возьмет дефолт для локалки
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/inventory_db"

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore" # Игнорировать лишние переменные в .env
    )

settings = Settings()