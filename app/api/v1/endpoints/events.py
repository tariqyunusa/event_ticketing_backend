from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.event import Event
from app.models.user import User
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
    result = await db.execute(select(Evevnt))
    events = result.scalars().all()
    return events