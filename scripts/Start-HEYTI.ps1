$ErrorActionPreference = "Stop"

$heytiRoot = Split-Path -Parent $PSScriptRoot
$heytiPython = Join-Path $heytiRoot ".venv\Scripts\python.exe"
$heytiWeb = Join-Path $heytiRoot "apps\heyti-web"
$heytiUrl = "http://127.0.0.1:5173"
$heytiHealthUrl = "http://127.0.0.1:8765/health"

function Test-HeytiEndpoint {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Uri
    )

    try {
        Invoke-WebRequest `
            -Uri $Uri `
            -UseBasicParsing `
            -TimeoutSec 2 |
            Out-Null

        return $true
    }
    catch {
        return $false
    }
}

function Wait-HeytiEndpoint {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Uri,

        [Parameter(Mandatory = $true)]
        [string]$Name,

        [int]$Attempts = 30
    )

    for ($attempt = 1; $attempt -le $Attempts; $attempt++) {
        if (Test-HeytiEndpoint -Uri $Uri) {
            Write-Host "$Name disponible." -ForegroundColor Green
            return
        }

        Write-Host "Esperando ${Name}: intento $attempt de $Attempts..."
        Start-Sleep -Seconds 1
    }

    throw "$Name no respondió después de $Attempts segundos."
}

Write-Host "=== HEYTI CORE — ARRANQUE INTEGRADO ==="

if (-not (Test-Path $heytiPython)) {
    throw "No se encontró Python del proyecto: $heytiPython"
}

if (-not (Test-HeytiEndpoint -Uri $heytiHealthUrl)) {
    $securePassword = Read-Host `
        "Contraseña PostgreSQL para HEYTI" `
        -AsSecureString

    $passwordPointer = `
        [Runtime.InteropServices.Marshal]::SecureStringToBSTR(
            $securePassword
        )

    try {
        $env:HEYTI_DB_PASSWORD = `
            [Runtime.InteropServices.Marshal]::PtrToStringBSTR(
                $passwordPointer
            )

        $backendCommand = "Set-Location '$heytiRoot'; Write-Host '=== HEYTI CORE — GATEWAY HTTP ==='; & '$heytiPython' -m heyti.gateway.cli --host 127.0.0.1 --port 8765"

        Start-Process `
            powershell.exe `
            -WorkingDirectory $heytiRoot `
            -ArgumentList @(
                "-NoExit",
                "-NoProfile",
                "-Command",
                $backendCommand
            )
    }
    finally {
        Remove-Item `
            Env:\HEYTI_DB_PASSWORD `
            -ErrorAction SilentlyContinue

        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR(
            $passwordPointer
        )
    }

    Wait-HeytiEndpoint `
        -Uri $heytiHealthUrl `
        -Name "Gateway HEYTI"
}
else {
    Write-Host "Gateway HEYTI ya estaba disponible." -ForegroundColor Green
}

if (-not (Test-HeytiEndpoint -Uri $heytiUrl)) {
    $frontendCommand = "Set-Location '$heytiWeb'; Write-Host '=== HEYTI CORE — INTERFAZ WEB ==='; npm.cmd run dev -- --host 127.0.0.1 --port 5173"

    Start-Process `
        powershell.exe `
        -WorkingDirectory $heytiWeb `
        -ArgumentList @(
            "-NoExit",
            "-NoProfile",
            "-Command",
            $frontendCommand
        )

    Wait-HeytiEndpoint `
        -Uri $heytiUrl `
        -Name "Interfaz HEYTI"
}
else {
    Write-Host "Interfaz HEYTI ya estaba disponible." -ForegroundColor Green
}

Write-Host "`nHEYTI CORE está lista." -ForegroundColor Cyan
Start-Process $heytiUrl