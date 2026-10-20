// PM2 ecosystem config — production mode
// The React frontend is pre-built and served by FastAPI at http://127.0.0.1:8000
// (no separate frontend process needed in production)
//
// Usage:
//   pm2 start ecosystem.config.cjs   → start backend
//   pm2 stop all                      → stop all
//   pm2 logs                          → stream logs
//   pm2 delete all                    → remove processes
//   pm2 startup                       → auto-start on reboot (run as admin)

const path = require("path")
const ROOT   = __dirname
const PYTHON = "C:\\Program Files\\Python314\\python.exe"

module.exports = {
  apps: [
    {
      name: "slothtab-backend",
      script: PYTHON,
      args: "-m uvicorn backend.app:app --host 127.0.0.1 --port 8000",
      cwd: ROOT,
      watch: false,
      autorestart: true,
      env: { PYTHONUNBUFFERED: "1" },
      log_date_format: "YYYY-MM-DD HH:mm:ss",
      error_file: path.join(ROOT, "logs", "backend-error.log"),
      out_file:   path.join(ROOT, "logs", "backend-out.log"),
    },
  ],
}
