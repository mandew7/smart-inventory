import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine, Base
from app.models.product import Product
from app.models.category import Category
from app.models.stock_log import StockLog

from app.api.products import router as products_router
from app.api.categories import router as categories_router

app = FastAPI(title="Smart Inventory")

origins = [
    "http://127.0.0.1:5500",  # Ваш Live Server
    "http://localhost:5500",   # На случай, если обращаетесь через localhost
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           # Разрешить запросы с этих адресов
    allow_credentials=True,
    allow_methods=["*"],             # Разрешить все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],             # Разрешить все заголовки
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(products_router, prefix="/products", tags=["products"])
app.include_router(categories_router, prefix="/categories", tags=["categories"])

@app.get("/")
async def root():
    return {"status": "ok"}