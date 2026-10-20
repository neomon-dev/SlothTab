# SlothTab — stop all services
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" +
            [System.Environment]::GetEnvironmentVariable("Path","User")

if (Get-Command pm2 -ErrorAction SilentlyContinue) {
    pm2 stop all 2>$null
    pm2 delete all 2>$null
}

# Stop any lingering uvicorn processes on port 8000
$conn = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($conn) {
    Stop-Process -Id $conn.OwningProcess -Force -ErrorAction SilentlyContinue
}

Write-Host "🦥 SlothTab stopped." -ForegroundColor Cyan
