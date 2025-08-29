Param([string]$Command = "", [string]$Message = "")
$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path "$PSScriptRoot/.." ).Path
$Backend  = Join-Path $RepoRoot "backend"
$env:PYTHONPATH = $Backend
if (-not $env:DATABASE_URL) { $env:DATABASE_URL = "postgresql+psycopg://ppam:ppam@localhost:5432/ppam_db" }
Push-Location $Backend
try {
  switch ($Command) {
    "revision" { if (!$Message) { $Message = "autogen" }; alembic revision --autogenerate -m "$Message" }
    "upgrade"  { alembic upgrade head }
    "current"  { alembic current }
    default    { Write-Host "Uso: revision|upgrade|current" -ForegroundColor Yellow }
  }
} finally { Pop-Location }
