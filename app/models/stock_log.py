from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class StockLog(Base):
    __tablename__ = "stock_logs"

    id = Column(Integer, primary_key=True, index=True)
    # ДОБАВЛЕНО: ondelete="CASCADE"
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    action = Column(String)  # "sell" или "restock"
    quantity = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Указываем обратную связь
    product = relationship("Product", back_populates="stock_logs")