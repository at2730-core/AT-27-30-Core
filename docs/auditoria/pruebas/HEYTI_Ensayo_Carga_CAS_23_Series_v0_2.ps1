# Ensayo completo CAS v0.2 en una base temporal. NO conecta con at2730_core.
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
$SecArchive = Join-Path $PSScriptRoot 'HEYTI_Carga_Cruda_23_Series_PRUEBA.sql.gz'
$SecVerify = Join-Path $PSScriptRoot 'HEYTI_Verificacion_Carga_Cruda_23_Series_v0_1.sql'
$SecProjection = Join-Path $PSScriptRoot 'HEYTI_Proyeccion_23_Series_v0_1.sql'
$CasStage = Join-Path $PSScriptRoot 'HEYTI_Staging_Casillas_v0_2_PROPUESTA_NO_EJECUTAR.sql'
$CasArchive = Join-Path $PSScriptRoot 'HEYTI_Carga_Cruda_CAS_23_Series_PRUEBA.sql.gz'
$CasProjection = Join-Path $PSScriptRoot 'HEYTI_Proyeccion_CAS_23_Series_v0_2.sql'
$CasVerify = Join-Path $PSScriptRoot 'HEYTI_Verificacion_CAS_23_Series_v0_2.sql'
$ExpectedSecArchive = '6d5dcad43463f63d97b8ccd8960a32c677e9d2a50c060738486d1767e083aedb'
$ExpectedSecSql = '595cba927cb272f0bb5cbc5f1ea58a83e73f0be0a2d8b7191294da03da33e1fb'
$ExpectedCasArchive = '4a4dfe6a41338c0d7101355cab970cb44f66e77311a5772bba12edc76a378b6d'
$ExpectedCasSql = 'e94c660a56b4377b7c0abb2435b44ec32cc5f5a69e2da5ba61720d71160f0072'
$ExpectedCasProjection = 'de1aefcbf33e989f5460aea6001a57d5abb7193d658659535aaa4f3ab192fa11'
foreach ($file in @($Psql,$CreateDb,$DropDb,$Territorial,$Electoral,$Stage,$Probe,$SecArchive,$SecVerify,$SecProjection,$CasStage,$CasArchive,$CasProjection,$CasVerify)) {
  if (-not (Test-Path -LiteralPath $file -PathType Leaf)) { throw "Archivo ausente: $file" }
}
foreach ($pair in @(@($SecArchive,$ExpectedSecArchive),@($CasArchive,$ExpectedCasArchive),@($CasProjection,$ExpectedCasProjection))) {
  if ((Get-FileHash -LiteralPath $pair[0] -Algorithm SHA256).Hash.ToLowerInvariant() -ne $pair[1]) {
    throw "SHA-256 incorrecto: $($pair[0])"
  }
}

$DbName = 'heyti_cas_full_probe_' + [guid]::NewGuid().ToString('N').Substring(0,12)
$SecTemp = Join-Path ([System.IO.Path]::GetTempPath()) ($DbName + '_sec.sql')
$CasTemp = Join-Path ([System.IO.Path]::GetTempPath()) ($DbName + '_cas.sql')
$Created = $false
function Expand-Checked([string]$Archive,[string]$Destination,[string]$Expected) {
  $inputStream = [System.IO.File]::OpenRead($Archive)
  try {
    $gzip = [System.IO.Compression.GzipStream]::new($inputStream,[System.IO.Compression.CompressionMode]::Decompress)
    try {
      $outputStream = [System.IO.File]::Create($Destination)
      try { $gzip.CopyTo($outputStream) } finally { $outputStream.Dispose() }
    } finally { $gzip.Dispose() }
  } finally { $inputStream.Dispose() }
  if ((Get-FileHash -LiteralPath $Destination -Algorithm SHA256).Hash.ToLowerInvariant() -ne $Expected) {
    throw "SQL descomprimido no coincide con SHA-256: $Destination"
  }
}
function Invoke-PsqlFile([string]$Path) {
  & $Psql -X -v ON_ERROR_STOP=1 -U postgres -d $DbName -f $Path
  if ($LASTEXITCODE -ne 0) { throw "Falló $Path; psql salió con $LASTEXITCODE" }
}
try {
  Expand-Checked $SecArchive $SecTemp $ExpectedSecSql
  Expand-Checked $CasArchive $CasTemp $ExpectedCasSql
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
  Invoke-PsqlFile $SecTemp
  Invoke-PsqlFile $SecVerify
  Invoke-PsqlFile $SecProjection
  Invoke-PsqlFile $CasStage
  Invoke-PsqlFile $CasTemp
  Invoke-PsqlFile $CasProjection
  Invoke-PsqlFile $CasVerify
  Write-Host 'ENSAYO CAS COMPLETO OK: 23 series, 179779 casillas, 4061868 celdas.'
}
finally {
  if ($Created) {
    Write-Host "Eliminando únicamente la base temporal: $DbName"
    & $DropDb -U postgres $DbName
    if ($LASTEXITCODE -ne 0) { Write-Warning "No se eliminó $DbName; revisa la salida de dropdb." }
  }
  foreach ($tempFile in @($SecTemp,$CasTemp)) {
    if (Test-Path -LiteralPath $tempFile) { Remove-Item -LiteralPath $tempFile -Force }
  }
}
