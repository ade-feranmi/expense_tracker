from typing import Annotated
from fastapi import APIRouter, Request, Depends, status
from fastapi import Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from models import User
from database import get_db
from crud import crud_create_user
from auth import create_access_token, authenticate_user_details
from schemas import UserCreate

router = APIRouter(
    prefix="",  
    tags=["UI Views"]
)
templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse)
def get_login_page(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="login.html"
    )


@router.post("/login", response_class=HTMLResponse)
def login_user_ui(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    form_data: OAuth2PasswordRequestForm = Depends()
):
    try:
        user = authenticate_user_details(
            db=db,
            email=form_data.username,
            password=form_data.password
        )

        token = create_access_token(
            data={"sub": str(user.id)}
        )
        response = RedirectResponse(
            url="/dashboard",
            status_code=status.HTTP_303_SEE_OTHER
        )
        response.set_cookie(
            key="access_token",
            value=f"Bearer {token}",
            httponly=True
        )
        return response
    
    except ValueError:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": "Invalid email or password"}
        )

@router.get("/signup", response_class=HTMLResponse)
def get_signup_page(request : Request):
    return templates.TemplateResponse(
        request=request,
        name="signup.html"    
    )

@router.post("/signup", response_class=HTMLResponse)
def signup_user_ui(
    request : Request,
    db : Annotated[Session, Depends(get_db)],
    email : str = Form(...),
    first_name : str = Form()
):
    try:


        token = create_access_token({"sub" : str(user.id)})
        response = RedirectResponse(
            url="dashboard",
            status_code=status.HTTP_303_SEE_OTHER
        )
        response.set_cookie(
            key="access_token",
            value=f"Bearer {token}",
            httponly=True
        )
        return response
    
    except ValueError as e:
        return templates.TemplateResponse(
            request=request,
            name="signup.html",
            context={"error" : str(e)}
        )

@router.get("/dashboard", response_class=HTMLResponse)
def get_dashboard_page(request:Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard"
    )


