# Ejecutar desde PowerShell en Windows. Crea y elimina una base NUEVA temporal.
# Requiere los dos SQL de este paquete junto a este archivo.
# No se conecta a at2730_core ni altera archivos del repositorio.
param(
  [string]$RepoRoot = 'D:\GitHub\AT-27-30-core',
  [string]$PgBin = 'C:\Program Files\PostgreSQL\18\bin'
)
$ErrorActionPreference = 'Stop'
$Psql = Join-Path $PgBin 'psql.exe'
$CreateDb = Join-Path $PgBin 'createdb.exe'
$DropDb = Join-Path $PgBin 'dropdb.exe'
$BaseTerritorial = Join-Path $RepoRoot 'database\ddl\001_create_territorial_base.sql'
$BaseElectoral = Join-Path $RepoRoot 'database\ddl\004_create_electoral_base.sql'
$StageDdl = Join-Path $PSScriptRoot 'HEYTI_Staging_Electoral_v0_1_PROPUESTA_NO_EJECUTAR.sql'
$ProbeSql = Join-Path $PSScriptRoot 'HEYTI_Prueba_Staging_Aislada_v0_1.sql'
foreach ($file in @($Psql,$CreateDb,$DropDb,$BaseTerritorial,$BaseElectoral,$StageDdl,$ProbeSql)) {
  if (-not (Test-Path -LiteralPath $file -PathType Leaf)) { throw "Archivo ausente: $file" }
}

$DbName = 'heyti_stage_probe_' + [guid]::NewGuid().ToString('N').Substring(0,12)
$Created = $false
function Invoke-PsqlFile([string]$Path) {
  & $Psql -X -v ON_ERROR_STOP=1 -U postgres -d $DbName -f $Path
  if ($LASTEXITCODE -ne 0) { throw "Falló archivo: $Path; psql salió con $LASTEXITCODE" }
}
try {
  Write-Host "Creando base temporal: $DbName"
  & $CreateDb -U postgres -T template0 $DbName
  if ($LASTEXITCODE -ne 0) { throw "createdb salió con $LASTEXITCODE" }
  $Created = $true
  & $Psql -X -v ON_ERROR_STOP=1 -U postgres -d $DbName -c 'CREATE SCHEMA territorial'
  if ($LASTEXITCODE -ne 0) { throw 'No se pudo crear esquema territorial de ensayo' }
  Invoke-PsqlFile $BaseTerritorial
  Invoke-PsqlFile $BaseElectoral
  Invoke-PsqlFile $StageDdl
  Invoke-PsqlFile $ProbeSql
  Write-Host 'ENSAYO OK: esquema y restricciones probados en base temporal.'
}
finally {
  if ($Created) {
    Write-Host "Eliminando únicamente la base temporal: $DbName"
    & $DropDb -U postgres $DbName
    if ($LASTEXITCODE -ne 0) {
      Write-Warning "No se eliminó la base temporal $DbName; bórrala tras revisar el error."
    }
  }
}
