# Ensayo aislado de carga cruda 15 ZIP/23 series en PostgreSQL 18.
# Los ZIP ya se cotejaron para generar el .sql.gz; este script comprueba su hash.
# Descarga en la MISMA carpeta: este ps1, .sql.gz, DDL v0.1, prueba DDL y verificación de carga.
param(
  [string]$RepoRoot = 'D:\GitHub\AT-27-30-core',
  [string]$PgBin = 'C:\Program Files\PostgreSQL\18\bin'
)
$ErrorActionPreference = 'Stop'
$Psql = Join-Path $PgBin 'psql.exe'
$CreateDb = Join-Path $PgBin 'createdb.exe'
$DropDb = Join-Path $PgBin 'dropdb.exe'
$Territorial = Join-Path $RepoRoot 'database\ddl\001_create_territorial_base.sql'
$Electoral = Join-Path $RepoRoot 'database\ddl\004_create_electoral_base.sql'
$Stage = Join-Path $PSScriptRoot 'HEYTI_Staging_Electoral_v0_1_PROPUESTA_NO_EJECUTAR.sql'
$Probe = Join-Path $PSScriptRoot 'HEYTI_Prueba_Staging_Aislada_v0_1.sql'
$Verify = Join-Path $PSScriptRoot 'HEYTI_Verificacion_Carga_Cruda_23_Series_v0_1.sql'
$Archive = Join-Path $PSScriptRoot 'HEYTI_Carga_Cruda_23_Series_PRUEBA.sql.gz'
$ExpectedArchive = '6d5dcad43463f63d97b8ccd8960a32c677e9d2a50c060738486d1767e083aedb'
$ExpectedSql = '595cba927cb272f0bb5cbc5f1ea58a83e73f0be0a2d8b7191294da03da33e1fb'
foreach ($file in @($Psql,$CreateDb,$DropDb,$Territorial,$Electoral,$Stage,$Probe,$Verify,$Archive)) {
  if (-not (Test-Path -LiteralPath $file -PathType Leaf)) { throw "Archivo ausente: $file" }
}
if ((Get-FileHash -LiteralPath $Archive -Algorithm SHA256).Hash.ToLowerInvariant() -ne $ExpectedArchive) {
  throw 'El archivo comprimido no coincide con el SHA-256 auditado.'
}

$DbName = 'heyti_raw_probe_' + [guid]::NewGuid().ToString('N').Substring(0,12)
$SqlTemp = Join-Path ([System.IO.Path]::GetTempPath()) ($DbName + '.sql')
$Created = $false
function Invoke-PsqlFile([string]$Path) {
  & $Psql -X -v ON_ERROR_STOP=1 -U postgres -d $DbName -f $Path
  if ($LASTEXITCODE -ne 0) { throw "Falló $Path; psql salió con $LASTEXITCODE" }
}
try {
  $inputStream = [System.IO.File]::OpenRead($Archive)
  try {
    $gzip = [System.IO.Compression.GzipStream]::new($inputStream,[System.IO.Compression.CompressionMode]::Decompress)
    try {
      $outputStream = [System.IO.File]::Create($SqlTemp)
      try { $gzip.CopyTo($outputStream) } finally { $outputStream.Dispose() }
    } finally { $gzip.Dispose() }
  } finally { $inputStream.Dispose() }
  if ((Get-FileHash -LiteralPath $SqlTemp -Algorithm SHA256).Hash.ToLowerInvariant() -ne $ExpectedSql) {
    throw 'El SQL descomprimido no coincide con el SHA-256 auditado.'
  }
  Write-Host "Creando base temporal: $DbName"
  & $CreateDb -U postgres -T template0 $DbName
  if ($LASTEXITCODE -ne 0) { throw "createdb salió con $LASTEXITCODE" }
  $Created = $true
  & $Psql -X -v ON_ERROR_STOP=1 -U postgres -d $DbName -c 'CREATE SCHEMA territorial'
  if ($LASTEXITCODE -ne 0) { throw 'No se pudo crear esquema territorial temporal' }
  Invoke-PsqlFile $Territorial
  Invoke-PsqlFile $Electoral
  Invoke-PsqlFile $Stage
  Invoke-PsqlFile $Probe
  Invoke-PsqlFile $SqlTemp
  Invoke-PsqlFile $Verify
  Write-Host 'ENSAYO DE CARGA CRUDA OK: 15 ZIP, 23 series, 73262 filas GTO.'
}
finally {
  if ($Created) {
    Write-Host "Eliminando únicamente la base temporal: $DbName"
    & $DropDb -U postgres $DbName
    if ($LASTEXITCODE -ne 0) { Write-Warning "No se eliminó $DbName; revisa la salida de dropdb." }
  }
  if (Test-Path -LiteralPath $SqlTemp) { Remove-Item -LiteralPath $SqlTemp -Force }
}
