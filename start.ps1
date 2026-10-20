# SlothTab — one-shot startup script (no Docker required)
# Runs:  backend on http://127.0.0.1:8000  (also serves built frontend)
#        dev frontend (optional) on http://localhost:5173
#
# Usage:
#   .\start.ps1           — production mode (backend only, frontend pre-built)
#   .\start.ps1 -Dev      — also launches frontend Vite dev server in a new window

param([switch]$Dev)
$ErrorActionPreference = "Stop"
$ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path

# Refresh PATH so node/npm/pm2 are found
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" +
            [System.Environment]::GetEnvironmentVariable("Path","User")

Write-Host "`n🦥 SlothTab startup" -ForegroundColor Cyan

# --- 1. Python deps ---
Write-Host "`n[1/3] Installing Python dependencies..." -ForegroundColor Yellow
pip install -r "$ROOT\requirements.txt" --quiet

# --- 2. Build frontend ---
Write-Host "`n[2/3] Building frontend..." -ForegroundColor Yellow
Set-Location "$ROOT\frontend"
npm install --silent
npm run build
Set-Location $ROOT

# --- 3. Launch backend ---
New-Item -ItemType Directory -Force "$ROOT\logs" | Out-Null
Write-Host "`n[3/3] Starting backend..." -ForegroundColor Yellow

if (Get-Command pm2 -ErrorAction SilentlyContinue) {
    pm2 delete all --silent 2>$null
    pm2 start "$ROOT\ecosystem.config.cjs"
    Write-Host "`n✅ SlothTab is running via PM2!" -ForegroundColor Green
    Write-Host "   App: http://127.0.0.1:8000" -ForegroundColor White
    Write-Host "   pm2 logs        → live log stream"
    Write-Host "   pm2 stop all    → stop everything"
    Write-Host "   pm2 delete all  → remove from PM2`n"
} else {
    Start-Process python -ArgumentList "-m uvicorn backend.app:app --host 127.0.0.1 --port 8000" -WorkingDirectory $ROOT
    Write-Host "`n✅ SlothTab is running via Python!" -ForegroundColor Green
    Write-Host "   App: http://127.0.0.1:8000" -ForegroundColor White
    Write-Host "   Run .\stop.ps1 to stop.`n"
}

# --- Optional: launch Vite dev server in a separate window ---
if ($Dev) {
    Write-Host "Starting frontend dev server (http://localhost:5173)..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command",
        "Set-Location '$ROOT\frontend'; `$env:Path = [System.Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [System.Environment]::GetEnvironmentVariable('Path','User'); npm run dev"
}

Start-Process "http://127.0.0.1:8000"
