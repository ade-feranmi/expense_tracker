from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import Transaction
from schemas import ExpenseCreate,ExpenseUpdate,ExpenseOut

def query_expense(mpesa_code:str, db:Session) ->object:
    expense = db.query(Transaction).filter(Transaction.mpesa_code == mpesa_code).first()
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction Not Found"
        )
    return expense

def add_transaction(db:Session, payload:ExpenseCreate) -> ExpenseOut:
    try:
        new_expense = Transaction(**payload.model_dump())

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
    expenses=db.query(Transaction).all()
    return expenses

def get_transaction(db:Session, mpesa_code:str) -> ExpenseOut:
    search=query_expense(mpesa_code, db=db)
    return search

def edit_transaction(db:Session, mpesa_code:str, payload:ExpenseUpdate) -> ExpenseOut:
    db_expense = query_expense(mpesa_code, db=db)

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


def delete_transaction(mpesa_code: str, db: Session) -> dict:
    expense = query_expense(mpesa_code, db=db)
    db.delete(expense)
    db.commit()
    
    return {"status": "success", "message": f"Transaction {mpesa_code} deleted successfully"}

