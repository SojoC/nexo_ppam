CODES = {
    "mg1": ("circuito", "Monagas 1"),
    "mgn1": ("circuito", "Monagas 1"),
    "mng1": ("circuito", "Monagas 1"),
    # TODO: añadir mg2, mg3, territorios, etc.
}

def parse_query(q: str):
    q = (q or "").lower().strip()
    exact = {}
    fuzzy = []
    for tok in q.split():
        if tok in CODES:
            field, value = CODES[tok]
            exact.setdefault(field, set()).add(value)
        else:
            fuzzy.append(tok)
    return exact, fuzzy
