import sys
import os
import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

# 1. Сначала добавляем путь к корню проекта, чтобы импорты 'app' работали
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 2. Импортируем настройки и базу
from app.core.config import settings  # Используем объект settings
from app.core.database import Base

# 3. ОБЯЗАТЕЛЬНО импортируем все модели, иначе Alembic не увидит таблицы!
from app.models.product import Product
from app.models.category import Category
from app.models.stock_log import StockLog # Не забудь лог, который мы создали

# Alembic Config
config = context.config

# Передаем URL из нашего pydantic-settings в конфиг Alembic
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection, 
        target_metadata=target_metadata,
        render_as_batch=True # Полезно для SQLite, не мешает для Postgres
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    # Здесь берем конфиг, где мы уже подменили sqlalchemy.url
    configuration = config.get_section(config.config_ini_section, {})
    
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Для асинхронности в Docker часто лучше использовать такой подход:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    if loop.is_running():
        # Если цикл уже запущен (редко для alembic, но бывает)
        import nest_asyncio
        nest_asyncio.apply()
        loop.run_until_complete(run_async_migrations())
    else:
        asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()