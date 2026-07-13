from typing import Annotated

from fastapi import APIRouter,status,Depends
from database import get_db
from sqlalchemy.orm import Session
from crud import add_transaction,get_transaction,view_transactions,edit_transaction,delete_transaction
from schemas import ExpenseCreate,ExpenseOut,ExpenseUpdate

router = APIRouter(
    prefix="/api/v1",
    tags=["Tracker Endpoints"] 
)

db = Annotated[Session, Depends(get_db)]

@router.get(
    "/expenses",
    response_model=list[ExpenseOut],
    status_code=status.HTTP_200_OK
)
def view_expenses(db: db):
    return view_transactions(db=db)

@router.get(
    "/expenses/{transaction_id}",
    response_model=ExpenseOut,
    status_code=status.HTTP_200_OK
)
def get_expense(transaction_id:str, db : db):
    return get_transaction(transaction_id=transaction_id, db=db)

@router.post(
    "/expenses",
    response_model=ExpenseOut,
    status_code=status.HTTP_201_CREATED
)
def add_expense(payload:ExpenseCreate, db:db):
    return add_transaction(payload=payload, db=db)

@router.patch(
    "/expenses/{transaction_id}",
    response_model=ExpenseOut,
    status_code=status.HTTP_201_CREATED
)
def edit_expense(transaction_id : str, db:db, payload:ExpenseUpdate):
    return edit_transaction(
        transaction_id=transaction_id,
        db=db,
        payload=payload
    )

@router.delete(
    "/expense/{transaction_id}",
    status_code=status.HTTP_200_OK
)
def delete_expense(transaction_id:str, db:db):
    return delete_transaction(transaction_id=transaction_id, db=db)

    
