from fastapi import APIRouter
from firebase_client import create_user, save_message

router = APIRouter()

@router.post("/register")
def register(email: str, password: str):
    uid = create_user(email, password)
    return {"uid": uid}

@router.post("/message")
def send_message(user_id: str, message: str):
    save_message(user_id, message)
    return {"status": "ok"}
