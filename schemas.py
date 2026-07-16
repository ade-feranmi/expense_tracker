from pydantic import BaseModel, ConfigDict,EmailStr,Field
from datetime import datetime
from decimal import Decimal
from enum import Enum

class TransactionSource(str, Enum):
    IMPORT = "IMPORT"
    MANUAL = "MANUAL"

class TransactionType(str, Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"

class ExpenseBase(BaseModel):
    type: TransactionType
    source: TransactionSource
    mpesa_code: str
    amount: Decimal
    description: str | None = None
    transaction_date: datetime

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseUpdate(BaseModel):
    type: TransactionType | None = None
    source: TransactionSource | None = None
    mpesa_code: str | None = None
    amount: Decimal | None = None
    description: str | None = None
    transaction_date: datetime | None = None

class ExpenseOut(ExpenseBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

class UserBase(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserCreate(UserBase):
    first_name: str
    last_name: str
    phone: str | None = None

class UserLogin(UserBase):
    pass

class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)

    first_name: str
    last_name: str
    phone: str | None = None
    id : int


class TokenOut(BaseModel):
    access_token : str
    token_type : str = "bearer"