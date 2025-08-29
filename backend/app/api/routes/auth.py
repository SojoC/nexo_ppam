from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

# Ajusta estos imports a tu árbol real de módulos
from app.db.session import get_db
from app.db.models import User
from app.core.security import verify_password, create_access_token

router = APIRouter(prefix="/api/v1", tags=["auth"])

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

def authenticate(db: Session, identifier: str, password: str) -> User | None:
    # Permite login con username O email
    user = (
        db.query(User)
        .filter((User.username == identifier) | (User.email == identifier))
        .first()
    )
    if not user or not user.password_hash:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

@router.post("/login", response_model=Token)
async def login(request: Request, db: Session = Depends(get_db)):
    """
    Acepta:
    - application/x-www-form-urlencoded  -> fields: username/password o email/password
    - application/json                   -> keys: username/password o email/password
    """
    ct = request.headers.get("content-type", "").lower()

    username_or_email = None
    password = None

    try:
        if "application/json" in ct:
            data = await request.json()
            username_or_email = (data.get("username") or data.get("email") or "").strip()
            password = (data.get("password") or "").strip()
        else:
            # form-urlencoded o multipart/form-data (por si acaso)
            form = await request.form()
            username_or_email = (form.get("username") or form.get("email") or "").strip()
            password = (form.get("password") or "").strip()
    except Exception:
        # fallback: intenta ambos por si headers venían mal
        try:
            data = await request.json()
            username_or_email = (data.get("username") or data.get("email") or "").strip()
            password = (data.get("password") or "").strip()
        except Exception:
            form = await request.form()
            username_or_email = (form.get("username") or form.get("email") or "").strip()
            password = (form.get("password") or "").strip()

    if not username_or_email or not password:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Missing username/email or password",
        )

    user = authenticate(db, username_or_email, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(sub=(user.uid or user.username or user.email))
    return {"access_token": token, "token_type": "bearer"}
    return verify_password(password, user.password_hash)

@router.post("/login", response_model=Token)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: "Session" = Depends(get_db) if get_db else None,
):
    """
    Recibe credenciales como x-www-form-urlencoded (username/password)
    Compatible con fetch usando URLSearchParams en el frontend.
    """
    username = form.username
    password = form.password

    ok = _authenticate_user(db, username, password) if db else False
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    token = create_access_token(sub=username)
    return {"access_token": token, "token_type": "bearer"}
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
