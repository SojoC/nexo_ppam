from unidecode import unidecode
try:
    from metaphone import doublemetaphone
except ImportError:
    from metaphone import doublemetaphone
import re

WORD_RE = re.compile(r"[a-zA-Záéíóúñü0-9]+")

def normalize(text: str) -> str:
    return unidecode((text or "").lower().strip())

def word_tokens(text: str):
    t = normalize(text)
    return WORD_RE.findall(t)

def chargrams(text: str, n: int = 3):
    t = normalize(text)
    t = f"__{t}__" if t else ""
    return {t[i:i+n] for i in range(max(0, len(t)-n+1))}

def phonetic(word: str):
    return set(filter(None, doublemetaphone(normalize(word))))

def contact_profile(contact: dict):
    campos = [contact.get("nombre",""), contact.get("circuito",""), contact.get("congregacion",""), contact.get("territorio",""), str(contact.get("telefono",""))]
    words = set(); grams = set(); phones = set()
    for c in campos:
        ws = word_tokens(c)
        words.update(ws)
        grams |= chargrams(c, 3)
        for w in ws:
            phones |= phonetic(w)
    return {"words": words, "grams": grams, "phones": phones}
