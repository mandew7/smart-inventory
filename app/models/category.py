from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base  # <--- ВОТ ЭТОЙ СТРОЧКИ НЕ ХВАТАЕТ

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # Связь с продуктами (убедись, что это тоже тут есть)
    products = relationship("Product", back_populates="category")