from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel

class TicketTypeCreate(BaseModel):
    name: str
    price: Decimal
    quantity_available: int
    sale_start: datetime
    sale_end: datetime
    
class TicketTypeResponse(BaseModel):
    id: int
    event_id: int
    name: str
    price: Decimal
    quantity_available: int
    sale_start: datetime
    sale_end: datetime
    model_config = {"from_attributes": True}
    