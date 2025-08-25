
import os
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import Depends, HTTPException, status, Request

# Carga de credenciales montadas en /keys/firebase.json (docker-compose)
cred_path = os.getenv("FIREBASE_CREDENTIALS", "/keys/firebase.json")
if not cred_path or not os.path.isfile(cred_path):
    raise RuntimeError(
        f"FIREBASE_CREDENTIALS no encontrado o inválido: {cred_path}. "
        "Revisa tu .env y el volumen en docker-compose."
    )

if not firebase_admin._apps:
    firebase_admin.initialize_app(credentials.Certificate(cred_path))

def require_firebase_user(request: Request):
    """
    Lee el encabezado Authorization: Bearer <ID_TOKEN>
    Verifica el token y retorna el 'uid' del usuario.
    """
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token faltante")

    id_token = auth_header.split(" ", 1)[1].strip()
    try:
        decoded = auth.verify_id_token(id_token)
        return decoded  # contiene uid, email, etc.
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
