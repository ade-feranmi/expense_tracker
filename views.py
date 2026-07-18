from typing import Annotated
from fastapi import APIRouter, Request, Depends, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from models import User
from database import get_db
from crud import crud_create_user
from auth import create_access_token, authenticate_user_details, decode_access_token
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
    form_data: OAuth2PasswordRequestForm = Depends(),
    remember_me: str | None = Form(None)
):
    form_data_info={
        "username" : form_data.username
    }

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
        max_age = 2592000 if remember_me else None

        response.set_cookie(
            key="access_token",
            value=f"Bearer {token}",
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=max_age
        )
        return response
    
    except ValueError:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": "Invalid email or password", "form":form_data_info}
        )

@router.get("/signup", response_class=HTMLResponse)
def get_signup_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="signup.html"    
    )

@router.post("/signup", response_class=HTMLResponse)
def signup_user_ui(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    email: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    phone: str | None = Form(None), 
    password: str = Form(...),
    confirm_password: str = Form(...),
    remember_me : str | None = Form(None),
    agree_terms : str | None = Form(None)
):
    form_data = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone
    }

    try:
        if not agree_terms:
            return templates.TemplateResponse(
                request=request,
                name="signup.html",
                context={"error": "you must agree to terms to registrer", "form" : form_data}
            )
        if password != confirm_password:
            return templates.TemplateResponse(
                request=request,
                name="signup.html",
                context={"error": "Passwords do not match", "form": form_data}
            )
        if len(password) < 8:
            return templates.TemplateResponse(
                request=request,
                name="signup.html",
                context={"error": "Password must be at least 8 characters long", "form": form_data}
            )
        
        user_in = UserCreate(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            password=password
        )
        new_user = crud_create_user(user_in=user_in, db=db)

        token = create_access_token({"sub": str(new_user.id)})

        response = RedirectResponse(
            url="/dashboard",
            status_code=status.HTTP_303_SEE_OTHER
        )
        max_age = 2592000 if remember_me else None

        response.set_cookie(
            key="access_token",
            value=f"Bearer {token}",
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=max_age
        )
        return response
    
    except ValueError as e:
        return templates.TemplateResponse(
            request=request,
            name="signup.html",
            context={"error": str(e), "form": form_data}
        )

@router.get("/dashboard", response_class=HTMLResponse)
def get_dashboard_page(
    request: Request,
    db: Annotated[Session, Depends(get_db)]
):
    cookie_token = request.cookies.get("access_token")
    if not cookie_token or not cookie_token.startswith("Bearer "):
        return RedirectResponse(
            url="/login",
            status_code=status.HTTP_303_SEE_OTHER
        )
    try:
        token = cookie_token.split()[1]

        user_id = decode_access_token(token)
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User records not Found")
        
        full_name = f"{user.first_name} {user.last_name}"
        
        return templates.TemplateResponse(
            request=request,
            name="dashboard.html",
            context={"name": full_name}
        )
    except Exception:
        response = RedirectResponse(
            url="/login",
            status_code=status.HTTP_303_SEE_OTHER
        )
        response.delete_cookie("access_token")
        return response
