Param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$AlembicArgs
)

# Establece PYTHONPATH al directorio actual y ejecuta Alembic con los argumentos dados
$env:PYTHONPATH = (Get-Location)
alembic @AlembicArgs