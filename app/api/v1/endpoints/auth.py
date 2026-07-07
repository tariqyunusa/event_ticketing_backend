from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import Token, UserCreate, UserResponse
from app.core.security import create_access_token, verify_password
from app.api.deps import get_current_user

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


@router.post("/login", response_model=Token)
async def login(payload: UserCreate, db: AsyncSession = Depends(get_db) ):
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"} 

@router.get("/me", response_model=UserResponse)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user