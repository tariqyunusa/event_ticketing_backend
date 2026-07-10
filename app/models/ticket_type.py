from datetime import datetime
from decimal import Decimal
from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class TicketType(Base):
    __tablename__ = "ticket_types"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    name: Mapped[str]
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    quantity_available: Mapped[int]
    sale_start: Mapped[datetime]
    sale_end: Mapped[datetime]
    