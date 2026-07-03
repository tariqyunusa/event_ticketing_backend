from datetime import datetime
from typing import Optional
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    venue: Mapped[str]
    start_time: Mapped[datetime]
    end_time: Mapped[datetime]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    