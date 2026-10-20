from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os

# Paths relative to project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
DB_PATH = os.path.join(DATA_DIR, "slothtab.db")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

from .db import init_db
from .routes import router
init_db()

app = FastAPI(
    title="SlothTab",
    description="Local-first AI productivity agent for intelligent file organization",
    version="0.1.0",
)

# CORS - allow local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)

FRONTEND_DIST = os.path.join(PROJECT_ROOT, "frontend", "dist")


@app.get("/api/health", tags=["root"])
async def health():
    """Health check endpoint."""
    return {"status": "ok", "message": "SlothTab is running"}


@app.get("/api/settings", tags=["settings"])
async def get_settings():
    """Get current settings from storage."""
    from .db import get_settings as db_get_settings
    return await db_get_settings()


@app.put("/api/settings", tags=["settings"])
async def put_settings(key: str, value: str):
    """Set a setting value."""
    from .db import set_setting as db_set_setting
    return await db_set_setting(key, value)


@app.get("/{full_path:path}", include_in_schema=False)
async def serve_frontend(full_path: str):
    """Serve the Vite build and support client-side routes in production."""
    if not os.path.isdir(FRONTEND_DIST):
        return {"detail": "Frontend build not found"}

    requested_path = os.path.join(FRONTEND_DIST, full_path)
    if full_path and os.path.isfile(requested_path):
        return FileResponse(requested_path)
    return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)