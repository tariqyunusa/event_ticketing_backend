from datetime import datetime
from pydantic import BaseModel

from app.models.ticket import TicketStatus

class TicketResponse(BaseModel):
    id: int
    order_id: int
    ticket_type_id: int
    owner_id: int
    qr_code: str
    status: TicketStatus
    created_at: datetime
    model_config = {"from_attributes": True}