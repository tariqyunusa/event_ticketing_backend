from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.api.deps import require_organizer
from app.models.user import User
from app.models.ticket import Ticket, TicketStatus
from app.models.ticket_type import TicketType
from app.models.event import Event
from app.schemas.ticket import TicketResponse

router = APIRouter()


@router.post("/tickets/{qr_code}/check-in", response_model=TicketResponse)
async def check_in_ticket(
    qr_code: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_organizer),    
):
    result = await db.execute(select(Ticket).where(Ticket.qr_code == qr_code))
    ticket = result.scalar_one_or_none()
    
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    result = await db.execute(select(TicketType).where(TicketType.id == ticket.ticket_type_id))
    ticket_type = result.scalar_one_or_none()
    
    result = await db.execute(select(Event).where(Event.id == ticket_type.event_id))
    event = result.scalar_one_or_none()
    
    if event.organizer_id != current_user.id:
        raise HTTPException(status_code=403, detail="This event does not belong to you")
    
    if ticket.status != TicketStatus.VALID:
        raise HTTPException(status_code=400, detail='This ticket has been used')
    
    ticket.status = TicketStatus.USED
    
    await db.commit()
    await db.refresh(ticket)
    return ticket

