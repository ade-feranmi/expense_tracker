from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import String, DECIMAL, DateTime, Enum as SQLEnum,ForeignKey,func
from database import Base

class TransactionSource(str, Enum):
    IMPORT = "IMPORT"
    MANUAL = "MANUAL"

class TransactionType(str, Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"
    
class Transaction(Base):
    __tablename__ = "transactions" 

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id : Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type: Mapped[TransactionType] = mapped_column(
        SQLEnum(TransactionType, name="transaction_type_enum"), nullable=False
    )
    source: Mapped[TransactionSource] = mapped_column(
        SQLEnum(TransactionSource, name="transaction_source_enum"), nullable=False
    )
    mpesa_code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    amount: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    description: Mapped[str] = mapped_column(String(100))
    transaction_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    user: Mapped["User"] = relationship(back_populates="transactions")

class User(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name : Mapped[str] = mapped_column(String(50), nullable=False)
    last_name : Mapped[str] = mapped_column(String(50), nullable=False)
    email : Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    hashed_password : Mapped[str] = mapped_column(String(250), nullable=False)
    phone : Mapped[str | None] = mapped_column(String(20), nullable=True, unique=True)
    created_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    transactions : Mapped[list["Transaction"]] = relationship(back_populates="user")
