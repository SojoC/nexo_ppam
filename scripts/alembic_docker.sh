#!/usr/bin/env bash
set -euo pipefail
SERVICE=${SERVICE:-api}
DB_URL=${DATABASE_URL:-"postgresql+psycopg://ppam:ppam@db:5432/ppam_db"}
docker compose exec -e DATABASE_URL="$DB_URL" "$SERVICE" bash -lc '
  set -e
  cd /app/backend
  export PYTHONPATH=/app/backend
  alembic upgrade head
'
