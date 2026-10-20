# SlothTab — stop all PM2 services
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" +
            [System.Environment]::GetEnvironmentVariable("Path","User")

pm2 stop all
pm2 delete all
Write-Host "🦥 SlothTab stopped." -ForegroundColor Cyan
