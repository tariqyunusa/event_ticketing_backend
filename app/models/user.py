from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column
import enum
from datetime import datetime
from sqlalchemy import func, Enum as SQLEnum


class UserRole(str, enum.Enum):
    BUYER = "buyer"
    ORGANIZER = "organizer"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    role: Mapped[UserRole] = mapped_column(
    SQLEnum(UserRole, values_callable=lambda x: [e.value for e in x]),
    default=UserRole.BUYER,
)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())