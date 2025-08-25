# Nexo_PPAM Fullstack (FastAPI + React + Docker)

## Levantar
1) Copia `.env.example` a `.env` (opcional).
2) `docker compose up -d db redis`
3) Espera ~10s (Postgres crea extensiones/tabla/demo).
4) `docker compose up -d api web`
5) API docs: http://localhost:8000/docs
6) Frontend: http://localhost:5173

### Login por defecto
- **username:** admin
- **password:** admin

## Estructura
- backend/ (FastAPI)
- frontend/ (Vite + React)
- docker-compose.yml
