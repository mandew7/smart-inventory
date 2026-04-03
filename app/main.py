from fastapi import FastAPI
# Импортируем роутеры напрямую из файлов
from app.api.products import router as products_router
from app.api.categories import router as categories_router

# Создаем экземпляр приложения
app = FastAPI(
    title="Smart Inventory System",
    description="Система управления складом с асинхронной базой данных",
    version="0.2.0"
)

# Подключаем роутер товаров
# Мы убираем prefix="/products" здесь, так как он уже прописан внутри самих файлов роутеров
app.include_router(products_router)
app.include_router(categories_router)

@app.get("/")
async def root():
    """
    Корневой эндпоинт для проверки работоспособности API.
    """
    return {
        "status": "online",
        "message": "Welcome to Smart Inventory API",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)