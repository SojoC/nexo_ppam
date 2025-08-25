from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Message
from app.messaging.manager import manager

router = APIRouter(prefix="/forms", tags=["forms"])

class S54(BaseModel):
    to_user_ids: list[str]
    data: dict

@router.post("/S54")
async def create_S54(payload: S54, db: Session = Depends(get_db)):
    msg = Message(body="Formulario S54", kind="form", metadata=payload.data)
    db.add(msg); db.commit(); db.refresh(msg)
    for uid in payload.to_user_ids:
        await manager.send_to_user(uid, {"type": "form", "data": msg.to_dict()})
    return {"id": msg.id}
