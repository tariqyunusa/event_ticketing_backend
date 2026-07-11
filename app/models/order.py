import enum
from datetime import datetime
from decimal import Decimal
from sqlalchemy import ForeignKey, Numeric, Enum as SQLEnum, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    
class Order(Base):
    __tablename__ = "orders"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    ticket_type_id: Mapped[int] = mapped_column(ForeignKey("ticket_types.id"))
    quantity: Mapped[int]
    total_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    status: Mapped[OrderStatus] = mapped_column(SQLEnum(OrderStatus, values_callable= lambda x: [e.value for e in x]), default=OrderStatus.PENDING)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    