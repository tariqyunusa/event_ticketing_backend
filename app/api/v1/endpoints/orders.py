from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.ticket_type import TicketType
from app.models.order import Order, OrderStatus
from app.models.ticket import Ticket, TicketStatus
from app.schemas.order import OrderCreate, OrderResponse

router = APIRouter()

@router.post("/orders", response_model=OrderResponse)
async def create_order(
    payload: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # step 2: locked read
    result = await db.execute(
        select(TicketType).where(TicketType.id == payload.ticket_type_id).with_for_update()
    )
    ticket_type = result.scalar_one_or_none()
    if ticket_type is None:
        raise HTTPException(status_code=404, detail="Ticket type not found")

    