from pydantic import BaseModel,ConfigDict
from datetime import datetime

class ExpenseBase(BaseModel):
    amount : float 
    description : str | None = None
    date : datetime
    transaction_id : str

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseUpdate(BaseModel):
    amount : float | None = None
    description : str | None = None
    date : datetime | None = None
    transaction_id : str | None = None

class ExpenseOut(ExpenseBase):
    model_config = ConfigDict(from_attributes=True)

    id : int

    
