from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# Настройка URL базы данных (для SQLite)
DATABASE_URL = "sqlite+aiosqlite:///./inventory.db"

# Создаем движок
engine = create_async_engine(DATABASE_URL, echo=True)

# Создаем фабрику сессий
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

# ТА САМАЯ ФУНКЦИЯ, КОТОРУЮ ОН НЕ МОЖЕТ НАЙТИ
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session