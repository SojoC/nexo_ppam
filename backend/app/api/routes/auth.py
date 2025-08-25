from app.core.firebase import require_firebase_user
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/whoami")
def whoami(user = Depends(require_firebase_user)):
    return {"uid": user.get("uid"), "email": user.get("email")}
    
@router.get("/me")
def me(user=Depends(require_firebase_user)):
    # user es el dict decodificado del token (uid, email, etc.)
    return {"uid": user.get("uid"), "email": user.get("email")}
