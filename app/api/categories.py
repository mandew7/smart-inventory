from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=CategoryResponse)
async def create_category(category: CategoryCreate, db: AsyncSession = Depends(get_db)):
    # Проверяем, нет ли уже категории с таким именем
    result = await db.execute(select(Category).where(Category.name == category.name))
    existing_category = result.scalars().first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Category already exists")
    
    new_category = Category(name=category.name)
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return new_category

@router.get("/", response_model=list[CategoryResponse])
async def get_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category))
    categories = result.scalars().all()
    return categories

@router.delete("/{category_id}")
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    # 1. Ищем категорию
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")

    # 2. Проверяем, есть ли в ней товары (опционально, если хочешь выдать красивую ошибку)
    product_check = await db.execute(select(Product).where(Product.category_id == category_id))
    if product_check.scalars().first():
        raise HTTPException(
            status_code=400, 
            detail="Нельзя удалить категорию, в которой есть товары. Сначала удалите или переместите товары."
        )

    # 3. Удаляем
    await db.delete(category)
    await db.commit()
    return {"message": f"Категория '{category.name}' успешно удалена"}