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

    result = await db.execute(
        select(TicketType).where(TicketType.id == payload.ticket_type_id).with_for_update()
    )
    ticket_type = result.scalar_one_or_none()
    if ticket_type is None:
        raise HTTPException(status_code=404, detail="Ticket type not found")

    if payload.quantity > ticket_type.quantity_available:
        raise HTTPException(status_code=400, detail="Not enough tickets available")
    
    ticket_type.quantity_available -= payload.quantity
    total_price = ticket_type.price * payload.quantity
    
    new_order = Order(
        user_id=current_user.id,
        ticket_type_id=ticket_type.id,
        quantity=payload.quantity,
        total_price=total_price,
        status=OrderStatus.PENDING,
    )
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    
    for _ in range(payload.quantity):
        new_ticket = Ticket(
            order_id=new_order.id,
            ticket_type_id=ticket_type.id,
            owner_id=current_user.id,
            status=TicketStatus.VALID
        )
        db.add(new_ticket)
    await db.commit()
    return new_order
   