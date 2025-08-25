from typing import Dict, Set
from fastapi import WebSocket
from collections import defaultdict

class ConnectionManager:
    def __init__(self):
        self.user_sockets: Dict[str, Set[WebSocket]] = defaultdict(set)
        self.channel_subs: Dict[str, Set[WebSocket]] = defaultdict(set)

    async def connect(self, user_id: str, ws: WebSocket):
        await ws.accept()
        self.user_sockets[user_id].add(ws)

    def disconnect(self, user_id: str, ws: WebSocket):
        self.user_sockets[user_id].discard(ws)
        for subs in self.channel_subs.values():
            subs.discard(ws)

    def subscribe(self, channel: str, ws: WebSocket):
        self.channel_subs[channel].add(ws)

    async def send_to_user(self, user_id: str, payload: dict):
        for ws in list(self.user_sockets.get(user_id, [])):
            await ws.send_json(payload)

    async def broadcast_channel(self, channel: str, payload: dict):
        for ws in list(self.channel_subs.get(channel, [])):
            await ws.send_json(payload)

manager = ConnectionManager()
