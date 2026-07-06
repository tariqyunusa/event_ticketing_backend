from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
async def signup(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    ##check if user already exists
    result = await db.execute(select(User).where(User.email == payload.email))
    
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    ##hash Password
    hashed_pw = hash_password(payload.password)
    
    #create new user
    new_user = User(email=payload.email, hashed_password=hashed_pw)
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user