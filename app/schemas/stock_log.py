from pydantic import BaseModel
from datetime import datetime

class StockLogResponse(BaseModel):
    id: int
    product_id: int
    action: str
    quantity: int
    timestamp: datetime

    class Config:
        from_attributes = True