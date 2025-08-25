from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from firebase_admin import auth
from app.messaging.manager import manager

router = APIRouter()

@router.websocket("/ws")
async def ws_endpoint(ws: WebSocket, token: str):
    # valida el ID token de Firebase
    try:
        decoded = auth.verify_id_token(token)
        user_id = decoded["uid"]
    except Exception:
        await ws.close(code=4401)  # Unauthorized
        return

    await ws.accept()
    await manager.connect(user_id, ws)
    try:
        while True:
            data = await ws.receive_json()
            t = data.get("type")
            if t == "subscribe":
                manager.subscribe(data["channel"], ws)
            elif t == "ack_read":
                pass
    except WebSocketDisconnect:
        manager.disconnect(user_id, ws)
