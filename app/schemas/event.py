from pydantic import BaseModel
from datetime import datetime

class EventCreate(BaseModel):
    name: str
    description: str
    venue: str
    start_time: datetime
    end_time: datetime
    
class EventResponse(BaseModel):
    id: int
    name: str
    description: str
    venue: str
    start_time: datetime
    end_time: datetime
    created_at: datetime
    model_config = {"from_attributes": True}