## Migraciones Alembic en Windows

Para crear y aplicar migraciones de base de datos con Alembic en Windows, usa el script automatizado:

1. Abre PowerShell y navega a la carpeta backend:
	```powershell
	cd backend
	```

2. Para crear una nueva migración automática:
	```powershell
	./scripts/alembic_win.ps1 -AlembicArgs revision --autogenerate -m "mensaje"
	```
	Ejemplo:
	```powershell
	./scripts/alembic_win.ps1 -AlembicArgs revision --autogenerate -m "init"
	```

3. Para aplicar las migraciones:
	```powershell
	./scripts/alembic_win.ps1 -AlembicArgs upgrade head
	```

> Nota: No uses comillas simples ni dobles alrededor de toda la cadena de argumentos, solo en el mensaje si es necesario. Si tienes problemas con rutas o imports, asegúrate de estar en la carpeta backend y que el script tenga permisos de ejecución.
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
