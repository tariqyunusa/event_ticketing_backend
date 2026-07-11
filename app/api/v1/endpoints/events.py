from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.event import Event
from app.models.user import User
from app.models.ticket_type import TicketType
from app.schemas.ticket_type import TicketTypeCreate, TicketTypeResponse
from app.schemas.event import EventCreate, EventResponse
from app.api.deps import require_organizer

router = APIRouter()

@router.post("/events", response_model=EventResponse)
async def create_event(payload: EventCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_organizer)):
    new_event = Event(
        name=payload.name,
        description=payload.description,
        venue=payload.venue,
        start_time=payload.start_time,
        end_time=payload.end_time,
        
        organizer_id=current_user.id
        
    )
    db.add(new_event)
    await db.commit()
    await db.refresh(new_event)
    return new_event

@router.get("/events", response_model=list[EventResponse])
async def list_events(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Event))
    events = result.scalars().all()
    return events

@router.get("/events/{event_id}", response_model=EventResponse)
async def get_event(event_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.post("/events/{event_id}/ticket-types", response_model=TicketTypeResponse)
async def create_ticket_type(
    event_id: int, payload: TicketTypeCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_organizer)):
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()
    if event is None: 
        raise HTTPException(status_code=404, detail="Event not found")
    if event.organizer_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not own this event")
    
    new_ticket_Type = TicketType(
        event_id=event_id,
        name=payload.name,
        price=payload.price,
        quantity_available=payload.quantity_available,
        sale_start=payload.sale_start,
        sale_end=payload.sale_end
    )
    db.add(new_ticket_Type)
    await db.commit()
    await db.refresh(new_ticket_Type)
    return new_ticket_Type

@router.get("/events/{event_id}/ticket-types", response_model=list[TicketTypeResponse])
async def list_ticket_types(event_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    ticket_result = await db.execute(select(TicketType).where(TicketType.event_id == event_id))
    ticket_types = ticket_result.scalars().all()
    return ticket_types