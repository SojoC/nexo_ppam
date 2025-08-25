from typing import List, Optional
from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel
from sqlalchemy import select, func, text
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.db.models import Contact

router = APIRouter()

class ContactOut(BaseModel):
    id: int
    nombre: str | None = None
    telefono: str | None = None
    circuito: str | None = None
    congregacion: str | None = None
    territorio: str | None = None
    privilegios: str | None = None
    class Config:
        from_attributes = True

def _ilike_any(db: Session, term: str):
    # Usa immutable_unaccent si existe; de lo contrario, unaccent normal; si no, identidad.
    # Para simplificar, asumimos que init.sql creó immutable_unaccent().
    u = func.immutable_unaccent
    t = f"%{term}%"
    return (
        (u(Contact.nombre).ilike(u(t))) |
        (u(Contact.congregacion).ilike(u(t))) |
        (u(Contact.circuito).ilike(u(t))) |
        (Contact.telefono.ilike(t))
    )

@router.get("/", response_model=List[ContactOut])
def list_contacts(
    db: Session = Depends(get_db),
    q: Optional[str] = None,
    congregacion: Optional[str] = None,
    circuito: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    order_by: str = "nombre",
    direction: str = "asc",
):
    stmt = select(Contact)
    if q:
        # Soporta términos separados por espacio
        for token in q.split():
            stmt = stmt.where(_ilike_any(db, token))
    if congregacion:
        stmt = stmt.where(func.immutable_unaccent(Contact.congregacion) == func.immutable_unaccent(congregacion))
    if circuito:
        stmt = stmt.where(func.immutable_unaccent(Contact.circuito) == func.immutable_unaccent(circuito))

    order_col = {
        "nombre": Contact.nombre,
        "telefono": Contact.telefono,
        "circuito": Contact.circuito,
        "congregacion": Contact.congregacion,
    }.get(order_by, Contact.nombre)

    if direction.lower() == "desc":
        order_col = order_col.desc()
    else:
        order_col = order_col.asc()

    stmt = stmt.order_by(order_col).limit(limit).offset(offset)
    rows = db.execute(stmt).scalars().all()
    return rows

@router.get("/suggest", response_model=List[str])
def suggest(
    db: Session = Depends(get_db),
    q: str = "",
    max_items: int = 8,
):
    if not q:
        return []
    token = f"{q}%"
    u = func.immutable_unaccent
    stmt = select(Contact.nombre).where(u(Contact.nombre).ilike(u(token))).order_by(Contact.nombre.asc()).limit(max_items)
    names = [r[0] for r in db.execute(stmt).all() if r[0]]
    return names

@router.get("/by-phone", response_model=List[ContactOut])
def by_phone(
    db: Session = Depends(get_db),
    phone: str = "",
    match: str = "prefix"  # 'exact' | 'prefix'
):
    if not phone:
        return []
    if match == "exact":
        stmt = select(Contact).where(Contact.telefono == phone).limit(20)
    else:
        stmt = select(Contact).where(Contact.telefono.ilike(f"{phone}%")).limit(50)
    return db.execute(stmt).scalars().all()

@router.get("/stats")
def stats(db: Session = Depends(get_db), top_k: int = 10):
    # Top por congregación y circuito
    cong = db.execute(select(Contact.congregacion, func.count().label("n"))
                      .group_by(Contact.congregacion)
                      .order_by(func.count().desc())
                      .limit(top_k)).all()
    circ = db.execute(select(Contact.circuito, func.count().label("n"))
                      .group_by(Contact.circuito)
                      .order_by(func.count().desc())
                      .limit(top_k)).all()
    return {
        "top_congregaciones": [{"congregacion": c[0], "count": c[1]} for c in cong],
        "top_circuitos": [{"circuito": c[0], "count": c[1]} for c in circ],
    }

@router.get("/stats.csv")
def stats_csv(db: Session = Depends(get_db), top_k: int = 10, delimiter: str = "comma", excel_compat: bool = False):
    sep = ";" if delimiter == "semicolon" else ","
    data = stats(db=db, top_k=top_k)
    lines = ["tipo"+sep+"valor"+sep+"count"]
    for item in data["top_congregaciones"]:
        lines.append("congregacion"+sep+f"{item['congregacion'] or ''}"+sep+str(item["count"]))
    for item in data["top_circuitos"]:
        lines.append("circuito"+sep+f"{item['circuito'] or ''}"+sep+str(item["count"]))
    csv_text = "\n".join(lines)
    if excel_compat:
        csv_text = "\ufeff" + csv_text  # BOM UTF-8
    return Response(content=csv_text, media_type="text/csv; charset=utf-8")

@router.get("/export")
def export_contacts(
    db: Session = Depends(get_db),
    q: Optional[str] = None,
    congregacion: Optional[str] = None,
    circuito: Optional[str] = None,
    delimiter: str = "comma",
    excel_compat: bool = False,
):
    rows = list_contacts(db=db, q=q, congregacion=congregacion, circuito=circuito, limit=2000)
    sep = ";" if delimiter == "semicolon" else ","
    lines = ["id"+sep+"nombre"+sep+"telefono"+sep+"circuito"+sep+"congregacion"+sep+"territorio"+sep+"privilegios"]
    for c in rows:
        def f(x): return (x or "").replace(sep, " ")
        lines.append(sep.join([
            str(c.id), f(c.nombre), f(c.telefono), f(c.circuito), f(c.congregacion), f(c.territorio), f(c.privilegios)
        ]))
    csv_text = "\n".join(lines)
    if excel_compat:
        csv_text = "\ufeff" + csv_text
    return Response(
        content=csv_text,
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": "attachment; filename=contacts.csv"}
    )
