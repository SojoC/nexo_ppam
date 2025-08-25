from sqlalchemy.orm import Session
from app.db.models import SearchFeedback
from .matcher import set_weights

COUNTS = {"ok": 0, "bad": 0}

def record_feedback(db: Session, query: str, chosen_contact_id: int, user_id: int | None, ok: bool):
    fb = SearchFeedback(query=query, chosen_contact_id=chosen_contact_id, user_id=user_id, ok=ok)
    db.add(fb); db.commit()
    COUNTS["ok" if ok else "bad"] += 1
    total = COUNTS["ok"] + COUNTS["bad"]
    if total and total % 20 == 0:
        ratio = COUNTS["ok"] / total
        new = {"token": 1.0 + ratio*0.6, "exact": 1.5 + (1.0-ratio)}
        set_weights(new)
