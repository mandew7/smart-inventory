from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    stock = Column(Integer, default=0)
    
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    
    # Добавляем lazy="selectin" — это важно для асинхронной работы!
    category = relationship("Category", back_populates="products", lazy="selectin")