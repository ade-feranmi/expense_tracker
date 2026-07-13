from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import Expense
from schemas import ExpenseCreate,ExpenseOut,ExpenseUpdate

def query_expense(transaction_id:str, db:Session) ->object:
    expense = db.query(Expense).filter(Expense.transaction_id == transaction_id).first()
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction Not Found"
        )
    return expense

def add_transaction(db:Session, payload:ExpenseCreate) -> ExpenseOut:
    try:
        new_expense = Expense(**payload.model_dump())

        db.add(new_expense)
        db.commit()
        db.refresh(new_expense)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= {"error" : "database integrity violation"}
        )
    return new_expense


def view_transactions(db:Session) -> list[ExpenseOut]:
    expenses=db.query(Expense).all()
    return expenses

def get_transaction(db:Session, transaction_id:str) -> ExpenseOut:
    search=query_expense(transaction_id, db=db)
    return search

def edit_transaction(db:Session, transaction_id:str, payload:ExpenseUpdate) -> ExpenseOut:
    db_expense = query_expense(transaction_id, db=db)

    update_data = payload.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_expense, key, value)

    try:
        db.commit()
        db.refresh(db_expense)
    except IntegrityError:
        db.rollback() 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "database integrity violation"}
        )
    
    return db_expense


def delete_transaction(transaction_id: str, db: Session) -> dict:
    expense = query_expense(transaction_id, db=db)
    db.delete(expense)
    db.commit()
    
    return {"status": "success", "message": f"Transaction {transaction_id} deleted successfully"}

