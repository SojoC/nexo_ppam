
from sqlalchemy import select, or_, func, text
from sqlalchemy.orm import Session
from typing import Optional, Literal
from datetime import datetime
from app.db.models import Contact, SearchLog
# --- Logging y búsqueda por teléfono ---
def _only_digits(s: str) -> str:
    return "".join(ch for ch in (s or "") if ch.isdigit())

def log_query(db: Session, term_raw: str, normalized_tokens: list[str], hit_count: int) -> None:
    try:
        row = SearchLog(
            term_raw=term_raw or "",
            term_norm=" ".join(normalized_tokens) if normalized_tokens else (term_raw or ""),
            tokens=normalized_tokens or [],
            hit_count=hit_count,
            created_at=datetime.utcnow(),
        )
        db.add(row)
        db.commit()
    except Exception:
        db.rollback()  # logging jamás debe tumbar la búsqueda

def search_by_phone(
    db: Session,
    phone: str,
    match: Literal["exact", "prefix", "contains"] = "exact",
    limit: int = 50,
) -> list[Contact]:
    """
    Compara por dígitos: regexp_replace(telefono, '\\D', '', 'g')
    - exact   : igual a los dígitos
    - prefix  : empieza por los dígitos
    - contains: contiene los dígitos
    """
    digits = _only_digits(phone)
    if not digits:
        return []

    phone_digits_expr = func.regexp_replace(Contact.telefono, r'[^0-9]', '', 'g')

    if match == "exact":
        cond = (phone_digits_expr == digits)
    elif match == "prefix":
        cond = phone_digits_expr.like(f"{digits}%")
    else:
        cond = phone_digits_expr.like(f"%{digits}%")

    stmt = (
        select(Contact)
        .where(cond)
        .order_by(Contact.nombre.asc())
        .limit(limit)
    )
    return db.execute(stmt).scalars().all()

# Fonética opcional
try:
    from metaphone import doublemetaphone
except Exception:
    doublemetaphone = None

ABBR = {
    "SJ": "sojo",
    "MRQZ": "marquez",
    "MRN": "mirian",
    "CRL": "carlos",
    "MG": "monagas",
}

def _clean(s: str) -> str:
    return (s or "").strip()

def _tokens(s: str) -> list[str]:
    s = _clean(s).replace(",", " ").replace("-", " ").replace("_", " ")
    return [t for t in s.split() if t]

def _expand_abbr(tokens: list[str]) -> list[str]:
    out = []
    for t in tokens:
        t_up = t.upper()
        if t_up in ABBR:
            out.append(ABBR[t_up])
        else:
            if t_up == "MG":
                out.append("monagas")
            else:
                out.append(t)
    return out

def _phonetic_key(s: str):
    if not doublemetaphone:
        return None
    return doublemetaphone(s)  # (primary, secondary)

def _ilike_unaccent(col, pattern):
    # Si no tienes unaccent, cambia por: return col.ilike(pattern)
    return func.unaccent(col).ilike(func.unaccent(pattern))

def search_contacts(
    db: Session,
    term: str = "",
    limit: int = 50,
    offset: int = 0,
    filtro_circuito: Optional[str] = None,
    filtro_congregacion: Optional[str] = None,
    order_by: str = "nombre",
    direction: str = "asc",
):
    t = _clean(term)
    base_stmt = select(Contact)

    # Filtros opcionales
    filters = []
    if filtro_circuito:
        filters.append(_ilike_unaccent(Contact.circuito, f"%{filtro_circuito}%"))
    if filtro_congregacion:
        filters.append(_ilike_unaccent(Contact.congregacion, f"%{filtro_congregacion}%"))

    if not t:
        stmt = base_stmt
        if filters:
            stmt = stmt.where(*filters)
        # Orden seguro
        col = Contact.nombre if order_by == "nombre" else Contact.telefono
        col = col.asc() if direction.lower() == "asc" else col.desc()
        stmt = stmt.order_by(col).limit(limit).offset(offset)
        return db.execute(stmt).scalars().all()

    toks = _expand_abbr(_tokens(t))
    like_terms = [f"%{tok}%" for tok in toks]

    # Buscar candidatos por coincidencia amplia
    or_conds = []
    for lk in like_terms:
        or_conds.extend([
            _ilike_unaccent(Contact.nombre, lk),
            _ilike_unaccent(Contact.congregacion, lk),
            _ilike_unaccent(Contact.circuito, lk),
            Contact.telefono.ilike(lk),
        ])

    stmt = base_stmt.where(or_(*or_conds))
    if filters:
        stmt = stmt.where(*filters)

    # Intento de orden por similitud (pg_trgm), si está disponible:
    # similarity(unaccent(nombre), unaccent('consulta'))
    query_str = " ".join(toks)
    similarity_expr = func.similarity(func.unaccent(Contact.nombre), func.unaccent(query_str))

    # Caeremos en ranking Python igual, pero tratar de ordenar ya en SQL ayuda mucho
    stmt = stmt.order_by(similarity_expr.desc(), Contact.nombre.asc())

    # Trae un pool amplio y luego rankea en Python
    stmt = stmt.limit(min(300, max(limit * 6, 120))).offset(0)
    candidates = db.execute(stmt).scalars().all()

    # Ranking Python
    def score(c: Contact) -> tuple:
        q = query_str.casefold()
        def norm(s: Optional[str]) -> str:
            return (s or "").casefold()
        fields = [norm(c.nombre), norm(c.congregacion), norm(c.circuito), norm(c.telefono)]
        blob = " | ".join(fields)
        s = 100
        if q == norm(c.telefono):
            s -= 50
        if q == norm(c.nombre):
            s -= 40
        if any(f.startswith(q) for f in fields):
            s -= 25
        if q in blob:
            s -= 15
        for tok in toks:
            tok_l = tok.casefold()
            if tok_l == norm(c.nombre):
                s -= 8
            if any(f.startswith(tok_l) for f in fields):
                s -= 5
            if tok_l in blob:
                s -= 3
        if doublemetaphone:
            nk = _phonetic_key(c.nombre or "") or ("", "")
            for tok in toks:
                tk = _phonetic_key(tok) or ("", "")
                if tk[0] and tk[0] == nk[0]:
                    s -= 4
                elif tk[1] and tk[1] == nk[1]:
                    s -= 2
        if any(tok.isdigit() for tok in toks) and norm(c.circuito):
            if any(tok in norm(c.circuito) for tok in toks if tok.isdigit()):
                s -= 4
        return (s, norm(c.nombre), c.id)

    ranked = sorted(candidates, key=score)
    return ranked[offset:offset+limit]

def suggest_terms(db: Session, term: str, max_items: int = 5):
    """
    Devuelve sugerencias tipo '¿quiso decir...?' basadas en:
    - Expansión de abreviaturas
    - Trigram similarity en nombre/congregación/circuito
    - Fonética opcional
    """
    raw = _clean(term)
    toks = _expand_abbr(_tokens(raw))
    normalized = toks.copy()
    q = " ".join(toks)

    # Usamos similarity si está pg_trgm (si no, igualmente funciona pero con menos precisión)
    sim_nombre = func.similarity(func.unaccent(Contact.nombre), func.unaccent(q))
    sim_cong   = func.similarity(func.unaccent(Contact.congregacion), func.unaccent(q))
    sim_circ   = func.similarity(func.unaccent(Contact.circuito), func.unaccent(q))

    stmt = (
        select(Contact.nombre.label("text"), sim_nombre.label("score"))
        .order_by(sim_nombre.desc()).limit(max_items)
    )
    n_hits = db.execute(stmt).all()

    stmt2 = (
        select(Contact.congregacion.label("text"), sim_cong.label("score"))
        .where(Contact.congregacion.isnot(None))
        .order_by(sim_cong.desc()).limit(max_items)
    )
    g_hits = db.execute(stmt2).all()

    stmt3 = (
        select(Contact.circuito.label("text"), sim_circ.label("score"))
        .where(Contact.circuito.isnot(None))
        .order_by(sim_circ.desc()).limit(max_items)
    )
    c_hits = db.execute(stmt3).all()

    items = []
    def _add(items_list, reason):
        for r in items_list:
            text_val = r[0]
            score_val = float(r[1] or 0.0)
            if text_val:
                items.append({"text": text_val, "reason": reason, "score": round(score_val, 4)})

    _add(n_hits, "nombre similar")
    _add(g_hits, "congregación similar")
    _add(c_hits, "circuito similar")

    # Quitar duplicados preservando orden
    seen = set()
    uniq = []
    for it in items:
        key = (it["text"], it["reason"])
        if key not in seen:
            seen.add(key)
            uniq.append(it)

    # Prioriza sugerencias de abreviación si aplica
    if normalized and normalized != _tokens(raw):
        joined = " ".join(normalized)
        uniq.insert(0, {"text": joined, "reason": "expansión de abreviaturas", "score": 1.0})

    return {
        "query": raw,
        "normalized": normalized,
        "suggestions": uniq[:max_items]
    }
