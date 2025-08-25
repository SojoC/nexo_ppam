from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from sqlalchemy import text
from app.db.session import SessionLocal
from app.core.auth import auth_required
from app.api.routes.login import router as login_router
from app.api.routes.contacts import router as contacts_router
from app.api.routes.messages import router as messages_router

app = FastAPI(title="Nexo_PPAM API", version="1.3.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en prod: lista tus dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- health / ready / raíz
@app.get("/")
def root():
    return {"ok": True, "name": app.title, "version": app.version}

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/ready")
def ready():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return {"ready": True}
    except Exception as e:
        return {"ready": False, "error": str(e)}

# ---- Rutas
# Login SIN auth (para obtener token)
app.include_router(login_router, prefix="/api/v1", tags=["Auth"])

# Rutas protegidas
app.include_router(
    contacts_router,
    prefix="/api/v1/contacts",
    tags=["Contacts"],
    dependencies=[Depends(auth_required)]
)

app.include_router(
    messages_router,
    prefix="/api/v1/messages",
    tags=["Messages"],
    dependencies=[Depends(auth_required)]
)

# ---- OpenAPI con Bearer por defecto
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title=app.title,
        version=app.version,
        description="API Nexo_PPAM",
        routes=app.routes,
    )
    schema.setdefault("components", {})["securitySchemes"] = {
        "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }
    schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = schema
    return app.openapi_schema

app.openapi = custom_openapi
