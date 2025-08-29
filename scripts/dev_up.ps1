$ErrorActionPreference = "Stop"
docker compose up -d --build
Start-Sleep -Seconds 2
docker compose ps
docker compose logs api --tail=100
