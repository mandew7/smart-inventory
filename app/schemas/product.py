from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.category import CategoryResponse

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    price: float = Field(..., gt=0)
    stock: int = Field(default=0, ge=0)
    # Добавляем сюда, чтобы поле было доступно и для создания, и для ответа
    category_id: Optional[int] = None 

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    category: Optional[CategoryResponse] = None
    class Config:
        from_attributes = True