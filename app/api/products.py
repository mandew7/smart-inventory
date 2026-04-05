from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.product import Product
from app.models.stock_log import StockLog
from app.schemas.product import ProductCreate, ProductResponse
from typing import List

# Префикс "/products" уже задан здесь. 
# Внутри функций мы пишем только то, что идет ПОСЛЕ него.
router = APIRouter(tags=["Products"])

# 1. Логи (Путь: GET /products/logs)
@router.get("/logs")
async def get_inventory_logs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(StockLog).order_by(StockLog.timestamp.desc()))
    return result.scalars().all()

# 2. Фильтр дефицита (Путь: GET /products/low-stock)
@router.get("/low-stock", response_model=List[ProductResponse])
async def get_low_stock_products(threshold: int = 5, db: AsyncSession = Depends(get_db)):
    """Товары, количество которых ниже порога."""
    result = await db.execute(select(Product).where(Product.stock < threshold))
    return result.scalars().all()

# 3. Получение ВСЕХ товаров (Путь: GET /products)
# Мы ставим "/", чтобы путь был ровно /products
@router.get("/", response_model=List[ProductResponse])
async def get_all_products(db: AsyncSession = Depends(get_db)):
    """Получить список всех товаров."""
    result = await db.execute(select(Product))
    return result.scalars().all()

# 4. Создание товара (Путь: POST /products)
@router.post("/", response_model=ProductResponse)
async def create_product(payload: ProductCreate, db: AsyncSession = Depends(get_db)):
    new_product = Product(**payload.model_dump())
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product

# 5. Получение ОДНОГО товара по ID (Путь: GET /products/{id})
@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product

# 6. Обновление (Путь: PATCH /products/{id})
@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product_data: ProductCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    
    for key, value in product_data.model_dump().items():
        setattr(product, key, value)
    
    await db.commit()
    await db.refresh(product)
    return product

# 7. Удаление (Путь: DELETE /products/{id})
@router.delete("/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    
    await db.delete(product)
    await db.commit()
    return {"message": f"Товар с id {product_id} успешно удален"}

# 8. Продажа (Путь: POST /products/{id}/sell)
@router.post("/{product_id}/sell", response_model=ProductResponse)
async def sell_product(product_id: int, quantity: int = 1, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    
    if not product or product.stock < quantity:
        raise HTTPException(status_code=400, detail="Ошибка продажи: недостаточно товара или ID неверен")

    # Уменьшаем остаток
    product.stock -= quantity

    # Создаем лог
    new_log = StockLog(
        product_id=product.id,
        action="sell",
        quantity=quantity
    )
    db.add(new_log)
    
    await db.commit()
    await db.refresh(product)
    return product