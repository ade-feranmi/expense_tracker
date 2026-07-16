from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException
from database import get_db
from models import User
from sqlalchemy.orm import Session
from auth import authenticate_user_details, get_current_user, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from crud import add_transaction, get_transaction, view_transactions, edit_transaction, delete_transaction, crud_create_user
from schemas import ExpenseCreate, ExpenseOut, ExpenseUpdate, UserCreate, UserOut, TokenOut

router = APIRouter(
    prefix="/api/v1",
    tags=["Tracker Endpoints"] 
)

db = Annotated[Session, Depends(get_db)]
current_active_user = Annotated[User, Depends(get_current_user)]

@router.get(
    "/transactions",
    response_model=list[ExpenseOut],
    status_code=status.HTTP_200_OK
)
def view_expenses(db: db, current_user: current_active_user):
    return view_transactions(db=db, current_user=current_user)


@router.get(
    "/transactions/{transaction_id}",
    response_model=ExpenseOut,
    status_code=status.HTTP_200_OK
)
def get_expense(transaction_id: str, current_user: current_active_user, db: db):
    try:
        return get_transaction(mpesa_code=transaction_id, db=db, current_user=current_user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.post(
    "/transactions",
    response_model=ExpenseOut,
    status_code=status.HTTP_201_CREATED
)
def add_expense(payload: ExpenseCreate, current_user: current_active_user, db: db):
    try:
        return add_transaction(payload=payload, db=db, current_user=current_user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

@router.patch(
    "/transactions/{transaction_id}",
    response_model=ExpenseOut,
    status_code=status.HTTP_200_OK
)
def edit_expense(transaction_id: str, current_user: current_active_user, db: db, payload: ExpenseUpdate):
    try:
        return edit_transaction(
            mpesa_code=transaction_id,
            db=db,
            payload=payload,
            current_user=current_user
        )
    except ValueError as e:
        if "not found" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    
@router.delete(
    "/transactions/{transaction_id}",
    status_code=status.HTTP_200_OK
)
def delete_expense(transaction_id: str, current_user: current_active_user, db: db):
    try:
        return delete_transaction(mpesa_code=transaction_id, db=db, current_user=current_user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.post(
    "/signup",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED
)
def signup_user(user_in: UserCreate, db: db) -> UserOut:
    try:
        user = crud_create_user(user_in=user_in, db=db)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.post(
    "/login",
    response_model=TokenOut,
    status_code=status.HTTP_200_OK
)
def authenticate_user(
    db: db,
    form_data: OAuth2PasswordRequestForm = Depends()
):
    try:
        user = authenticate_user_details(
            db=db,
            email=form_data.username,  
            password=form_data.password
        )
        
        token = create_access_token(data={"sub": str(user.id)})
        return TokenOut(
            access_token=token,
            token_type="bearer"
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e    
