from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_messages():
    return []

# --- Existing code below (disabled endpoints, models, etc.) ---
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.db.deps import get_db

# Endpoints deshabilitados temporalmente hasta que se definan los modelos Message, Channel, etc.

class SendRequest(BaseModel):
    to_user_ids: List[str] = Field(default_factory=list)
    to_channel: Optional[str] = None
    text: str
    kind: str = "text"
    meta: Dict[str, Any] | None = Field(default=None, alias="metadata")
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

# Endpoint deshabilitado temporalmente hasta que se definan los modelos Message, Channel, etc.
# @router.post("/send")
# async def send_message(payload: SendRequest, db: Session = Depends(get_db)):
#     # Persistir mensaje
#     channel_id = None
#     if payload.to_channel:
#         ch = db.query(Channel).first()
#         if not ch:
#             ch = Channel(type=ChannelType.group)
#             db.add(ch); db.commit(); db.refresh(ch)
#         channel_id = ch.id
#     msg = Message(channel_id=channel_id, body=payload.text, meta=payload.meta)
#     db.add(msg); db.commit(); db.refresh(msg)
#
#     # Fanout
#     if payload.to_channel:
#         await manager.broadcast_channel(payload.to_channel, {"type": "message", "data": msg.to_dict()})
#     for uid in payload.to_user_ids:
#         await manager.send_to_user(uid, {"type": "message", "data": msg.to_dict()})
#
#     return {"id": msg.id, "delivered_to": payload.to_user_ids, "channel": payload.to_channel}
