import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, Header, HTTPException, status
from jose import jwt, JWTError
from passlib.hash import bcrypt

JWT_SECRET = os.getenv("NEXO_JWT_SECRET", "devsecret_change_me")
JWT_ALG = os.getenv("NEXO_JWT_ALG", "HS256")
JWT_EXPIRE_MIN = int(os.getenv("NEXO_JWT_EXPIRE_MIN", "120"))

API_KEY_EXPECTED = os.getenv("NEXO_API_KEY")  # opcional

LOGIN_USER = os.getenv("NEXO_USER", "admin")
LOGIN_PASS = os.getenv("NEXO_PASS", "admin123")
PASS_HASH = os.getenv("NEXO_PASS_HASH")  # bcrypt hash opcional (tiene prioridad)

def verify_password(plain: str) -> bool:
    if PASS_HASH:
        try:
            return bcrypt.verify(plain, PASS_HASH)
        except Exception:
            return False
    return plain == LOGIN_PASS

def create_access_token(subject: str, minutes: int = JWT_EXPIRE_MIN) -> str:
    expire = datetime.utcnow() + timedelta(minutes=minutes)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)

def decode_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
    except JWTError:
        return None

class AuthContext:
    def __init__(self, subject: str, mode: str):
        self.subject = subject
        self.mode = mode  # "bearer" | "xapikey"

async def require_auth(
    authorization: Optional[str] = Header(default=None, alias="Authorization"),
    x_api_key: Optional[str] = Header(default=None, alias="X-API-Key"),
) -> AuthContext:
    # X-API-Key
    if x_api_key:
        if not API_KEY_EXPECTED or x_api_key != API_KEY_EXPECTED:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")
        return AuthContext(subject="apikey", mode="xapikey")

    # Bearer
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1].strip()
        data = decode_token(token)
        if not data or "sub" not in data:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return AuthContext(subject=data["sub"], mode="bearer")

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Auth required")
