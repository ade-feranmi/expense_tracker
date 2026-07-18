from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from schemas import UserLogin, UserCreate, ExpenseCreate, ExpenseUpdate, ExpenseOut
from auth import hash_password
from models import Transaction, User

def query_expense(
    mpesa_code: str, 
    db: Session, 
    current_user: User
) -> Transaction:
    
    expense = (
        db.query(Transaction)
        .filter(
            and_(
                Transaction.mpesa_code == mpesa_code,
                Transaction.user_id == current_user.id,
            )
        )
        .first()
    )
    if not expense:
        raise ValueError(f"Transaction with code {mpesa_code} not found")
    return expense

def add_transaction(
    db: Session, 
    payload: ExpenseCreate, 
    current_user: User
) -> ExpenseOut:
    try:
        new_expense = Transaction(user_id=current_user.id, **payload.model_dump())
        db.add(new_expense)
        db.commit()
        db.refresh(new_expense)
        return new_expense
    except IntegrityError as e:
        db.rollback()
        print(f"Database Integrity Error: {e}")
        raise ValueError("Transaction code already exists or data is invalid") from e

def view_transactions(
    db: Session, 
    current_user: User
) -> list[ExpenseOut]:
    return db.query(Transaction).filter(Transaction.user_id == current_user.id).all()

def get_transaction(db: Session, mpesa_code: str, current_user: User) -> ExpenseOut:
    return query_expense(mpesa_code=mpesa_code, db=db, current_user=current_user)

def edit_transaction(db: Session, mpesa_code: str, payload: ExpenseUpdate, current_user: User) -> ExpenseOut:
    db_expense = query_expense(mpesa_code=mpesa_code, db=db, current_user=current_user)

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_expense, key, value)
        
    try:
        db.commit()
        db.refresh(db_expense)
        return db_expense
    except IntegrityError as e:
        db.rollback()
        print(f"Database Integrity Error during update: {e}")
        raise ValueError("Update failed due to database integrity constraint") from e

def delete_transaction(mpesa_code: str, db: Session, current_user: User) -> dict:
    expense = query_expense(mpesa_code=mpesa_code, db=db, current_user=current_user)
    try:
        db.delete(expense)
        db.commit()
        return {"status": "success", "message": f"Transaction {mpesa_code} deleted successfully"}
    except Exception as e:
        db.rollback()
        raise ValueError("Failed to delete transaction") from e

def crud_create_user(
    db: Session,
    user_in: UserCreate
):
    try:
        user_data = user_in.model_dump()
        plain_password = user_data.pop("password")
        user_data["hashed_password"] = hash_password(plain_password)

        new_user = User(**user_data)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    except IntegrityError as e:
        db.rollback()
        print(f"Database Integrity Error: {e}")
        raise ValueError("email already exists") from e
