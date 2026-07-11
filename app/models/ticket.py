from datetime import datetime
import enum
from sqlalchemy import ForeignKey, Enum as SQLEnum, func
from sqlalchemy.orm import mapped_column, Mapped
from app.core.database import Base

class TicketStatus(str, enum.Enum):
    VALID = "valid"
    USED = "used"
    CANCELLED = "cancelled"
    
class Ticket(Base):
    
    __tablename__ = "tickets"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    ticket_type_id: Mapped[int] = mapped_column(ForeignKey("ticket_types.id"))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[TicketStatus] = mapped_column(SQLEnum(TicketStatus, values_callable= lambda x : [e.value for e in x]), default=TicketStatus.VALID)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())