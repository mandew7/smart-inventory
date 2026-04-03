from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse
from typing import List

router = APIRouter(prefix="/products", tags=["Products"])

# 1. Фильтр (выше всех)
@router.get("/low-stock", response_model=List[ProductResponse])
async def get_low_stock_products(threshold: int = 5, db: AsyncSession = Depends(get_db)):
    """Товары, количество которых ниже порога."""
    result = await db.execute(select(Product).where(Product.stock < threshold))
    return result.scalars().all()

# 2. Получение ВСЕХ товаров (теперь он появится в Swagger!)
@router.get("/", response_model=List[ProductResponse])
async def get_all_products(db: AsyncSession = Depends(get_db)):
    """Получить список всех товаров."""
    result = await db.execute(select(Product))
    return result.scalars().all()

# 3. Создание товара
@router.post("/", response_model=ProductResponse)
async def create_product(payload: ProductCreate, db: AsyncSession = Depends(get_db)):
    new_product = Product(**payload.model_dump())
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product

# 4. Получение ОДНОГО товара по ID
@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product

# 5. Обновление
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

# 6. Удаление
@router.delete("/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    
    await db.delete(product)
    await db.commit()
    return {"message": f"Товар с id {product_id} успешно удален"}

@router.post("/{product_id}/sell", response_model=ProductResponse)
async def sell_product(
    product_id: int, 
    quantity: int = 1, 
    db: AsyncSession = Depends(get_db)
):
    """
    Продажа товара: уменьшает остаток (stock) на указанное количество.
    """
    # Находим товар
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    
    # Проверяем, хватает ли товара на складе
    if product.stock < quantity:
        raise HTTPException(
            status_code=400, 
            detail=f"Недостаточно товара. В наличии: {product.stock}, запрашиваемо: {quantity}"
        )
    
    # Уменьшаем остаток
    product.stock -= quantity
    
    await db.commit()
    await db.refresh(product)  # Обновляем объект, чтобы подтянулась категория для ответа
    return product