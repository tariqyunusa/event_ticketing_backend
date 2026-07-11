from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from app.models.order import OrderStatus

class OrderCreate(BaseModel):
    ticket_type_id: int
    quantity: int
    
class OrderResponse(BaseModel):
    id: int
    user_id: int
    ticket_type_id: int
    quantity: int
    total_price: Decimal
    status: OrderStatus
    created_at: datetime
    model_config = {"from_attributes": True}