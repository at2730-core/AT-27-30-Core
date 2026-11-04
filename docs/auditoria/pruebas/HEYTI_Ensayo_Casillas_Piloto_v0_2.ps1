# Ensayo de casillas v0.2; crea y elimina únicamente una base temporal.
# Requiere los archivos de la proyección 23 series v0.1 y dos SQL v0.2 en esta carpeta.
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
$Projection = Join-Path $PSScriptRoot 'HEYTI_Proyeccion_23_Series_v0_1.sql'
$Archive = Join-Path $PSScriptRoot 'HEYTI_Carga_Cruda_23_Series_PRUEBA.sql.gz'
$CasSchema = Join-Path $PSScriptRoot 'HEYTI_Staging_Casillas_v0_2_PROPUESTA_NO_EJECUTAR.sql'
$CasPilot = Join-Path $PSScriptRoot 'HEYTI_Piloto_Casillas_DF18_21_v0_2.sql'
$ExpectedArchive = '6d5dcad43463f63d97b8ccd8960a32c677e9d2a50c060738486d1767e083aedb'
$ExpectedSql = '595cba927cb272f0bb5cbc5f1ea58a83e73f0be0a2d8b7191294da03da33e1fb'
$ExpectedCasSchema = 'e4f0b42de7cc5ad3c39b740757f0f4e5a1e4ea46f7ce976c95282351c7c2fdae'
$ExpectedCasPilot = 'f98b7a0194480387733c662621ff9cbeebbb3d1cf161ad881f211f33b9e1c911'
foreach ($file in @($Psql,$CreateDb,$DropDb,$Territorial,$Electoral,$Stage,$Probe,$Verify,$Projection,$Archive,$CasSchema,$CasPilot)) {
  if (-not (Test-Path -LiteralPath $file -PathType Leaf)) { throw "Archivo ausente: $file" }
}
foreach ($check in @(@($Archive,$ExpectedArchive),@($CasSchema,$ExpectedCasSchema),@($CasPilot,$ExpectedCasPilot))) {
  if ((Get-FileHash -LiteralPath $check[0] -Algorithm SHA256).Hash.ToLowerInvariant() -ne $check[1]) {
    throw "SHA-256 incorrecto: $($check[0])"
  }
}

$DbName = 'heyti_cas_probe_' + [guid]::NewGuid().ToString('N').Substring(0,12)
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
    throw 'El SQL crudo descomprimido no coincide con el SHA-256 auditado.'
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
  Invoke-PsqlFile $Projection
  Invoke-PsqlFile $CasSchema
  Invoke-PsqlFile $CasPilot
  Write-Host 'PILOTO CAS v0.2 OK: 5 casillas en 2 series; base viva intacta.'
}
finally {
  if ($Created) {
    Write-Host "Eliminando únicamente la base temporal: $DbName"
    & $DropDb -U postgres $DbName
    if ($LASTEXITCODE -ne 0) { Write-Warning "No se eliminó $DbName; revisa la salida de dropdb." }
  }
  if (Test-Path -LiteralPath $SqlTemp) { Remove-Item -LiteralPath $SqlTemp -Force }
}
