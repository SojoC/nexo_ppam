from datetime import datetime, timedelta, timezone
import os
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, Header, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel

from app.core.config import settings

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_scheme = HTTPBearer()

# Usuario dev por defecto (admin/admin)
DEV_USERNAME = os.getenv("DEV_USERNAME", "admin")
DEV_PASSWORD_HASH = pwd_context.hash(os.getenv("DEV_PASSWORD", "admin"))

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(sub: str, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode = {"sub": sub, "exp": exp}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def auth_required(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Auth required")
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub: Optional[str] = payload.get("sub")
        if not sub:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return {"user": sub}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

def authenticate_user(username: str, password: str) -> bool:
    if username != DEV_USERNAME:
        return False
    return verify_password(password, DEV_PASSWORD_HASH)
