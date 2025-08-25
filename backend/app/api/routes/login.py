from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.auth import authenticate_user, create_access_token, Token

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login", response_model=Token)
def login(payload: LoginRequest):
    if not authenticate_user(payload.username, payload.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(sub=payload.username)
    return {"access_token": token}
