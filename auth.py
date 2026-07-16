from datetime import datetime, timezone, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session
from models import User
from pwdlib import PasswordHash
from security import auth_settings
from database import get_db

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)

secret_key = auth_settings.secret_key
algorithm = auth_settings.algorithm
expiry_minutes = auth_settings.access_token_expiry_minutes


def create_access_token(data: dict) -> str:
    try:
        encode_data = data.copy()
        current_time = datetime.now(timezone.utc)
        expiry = current_time + timedelta(minutes=expiry_minutes)
    
        encode_data.update(
            {
                "exp": expiry,
                "iat": current_time
            }
        )
        return jwt.encode(
            encode_data,
            secret_key,
            algorithm=algorithm
        )
    except (jwt.PyJWTError, Exception) as e:
        print(f"Error: Token Generation Failed: {e}")
        raise RuntimeError("token creation failed") from e


def decode_access_token(token: str) -> str:
    try:
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=[algorithm]
        )
        user_id = payload.get("sub")

        if not user_id:
            print("ERROR:Sub claim missing from token payload")
            raise ValueError("Identity Missing from token")
        
        return user_id
        
    except jwt.PyJWTError as e:
        print(f"Error:Token validation failed:{e}")
        raise ValueError("Invalid token") from e



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")


def get_current_user(
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    try:
        user_id = decode_access_token(token)
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User Not Found")
        
        return user

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )        

def authenticate_user_details(
    db: Session, 
    email: str,
    password: str
) -> User:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise ValueError("Invalid email or password")
    
    return user
