from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String,DECIMAL,DateTime
from database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id : Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    date : Mapped[datetime] = mapped_column(DateTime,nullable=False)
    amount : Mapped[Decimal] = mapped_column(DECIMAL(10,2),nullable=False)
    description : Mapped[str] = mapped_column(String(100))
    transaction_id : Mapped[str] = mapped_column(String(50), nullable=False, unique=True)


