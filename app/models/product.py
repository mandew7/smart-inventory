from sqlalchemy import Column, Integer, String, Float, ForeignKey # Проверь этот импорт!
from sqlalchemy.orm import relationship
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    stock = Column(Integer, default=0)
    description = Column(String, nullable=True)
    
    # ВОТ ЗДЕСЬ БЫЛА ОШИБКА. Проверь, чтобы было именно так:
    category_id = Column(Integer, ForeignKey("categories.id")) 
    
    # Отношения (relationship)
    category = relationship("Category", back_populates="products")
    stock_logs = relationship("StockLog", back_populates="product", cascade="all, delete-orphan")