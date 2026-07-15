from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DECIMAL, DateTime, Enum as SQLEnum
from database import Base

class TransactionSource(str, Enum):
    IMPORT = "IMPORT"
    MANUAL = "MANUAL"

class TransactionType(str, Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"
    
class Transaction(Base):
    __tablename__ = "Transactions" \
    ""

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[TransactionType] = mapped_column(
        SQLEnum(TransactionType, name="transaction_type_enum"), nullable=False
    )
    source: Mapped[TransactionSource] = mapped_column(
        SQLEnum(TransactionSource, name="transaction_source_enum"), nullable=False
    )
    mpesa_code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    amount: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    description: Mapped[str] = mapped_column(String(100))
    transaction_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
