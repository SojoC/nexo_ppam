#!/usr/bin/env bash
set -euo pipefail

# Esperar DB
python - <<'PY'
import os, time, psycopg
url = os.environ.get("DATABASE_URL")
assert url, "DATABASE_URL no definido"
for i in range(60):
    try:
        with psycopg.connect(url, connect_timeout=3) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                break
    except Exception:
        time.sleep(1)
else:
    raise SystemExit("DB no disponible tras 60s")
PY

# Migraciones
alembic upgrade head

# Seed idempotente (crea usuario acme/acme y 300 contactos si no existen)
python -m app.db.seed

# API
exec uvicorn app.main:app --host ${UVICORN_HOST:-0.0.0.0} --port ${UVICORN_PORT:-8000}
