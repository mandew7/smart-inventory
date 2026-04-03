from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Эта строка должна совпадать с данными в docker-compose
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/inventory_management"
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()