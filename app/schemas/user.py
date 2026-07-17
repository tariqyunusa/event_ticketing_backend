from pydantic import BaseModel
from app.models.user import UserRole


class UserCreate(BaseModel):
    email: str
    password: str
    role: UserRole = UserRole.BUYER

class UserResponse(BaseModel):
    id: int
    email: str
    role: UserRole
    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str

