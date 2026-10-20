import os
import asyncio
import json
import re
from typing import List, Optional, Dict, Any

from fastapi import APIRouter, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse

from .db import init_db, get_connection, get_settings, set_setting
from .models import (
    FileInfo,
    AnalysisCreate,
    AnalysisInDB,
    OperationCreate,
    OperationInDB,
    SettingsResponse,
    SettingUpdate,
    FileOperationResult,
    DuplicateInfo,
    ApiResponse,
    ErrorResponse,
    SettingsResponse,
)
from .ai_provider import create_provider, AIProvider
from .file_processing import (
    get_file_info,
    sanitize_filename,
    process_file_async,
    get_supported_extensions,
    get_processor_for_file,
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_text_from_txt,
    extract_text_from_md,
    extract_text_from_image,
    compute_file_hash,
)

router = APIRouter(prefix="/api", tags=["slothtab"])


# --- Helper functions ---

def get_workspace_base() -> str:
    """Get the base workspace directory from settings or default to user downloads."""
    settings = asyncio.get_event_loop().run_until_complete(get_settings())
    base = settings.get("workspace_base", os.path.expanduser("~"))
    return os.path.normpath(base)


def is_safe_path(base: str, target: str) -> bool:
    """Validate that target path stays within base directory."""
    target_norm = os.path.normpath(target)
    base_norm = os.path.normpath(base)
    # Ensure target starts with base
    if not target_norm.startswith(base_norm + os.sep) and target_norm != base_norm:
        return False
    # Check for traversal
    if ".." in target_norm.split(os.sep):
        return False
    return True


def safe_os_rename(src: str, dst: str) -> None:
    """Safely rename/move a file, preventing overwrites."""
    if os.path.exists(dst) and src != dst:
        raise FileExistsError(f"Destination already exists: {dst}")
    os.rename(src, dst)


def safe_os_remove(filepath: str) -> None:
    """Safely remove a file."""
    if os.path.exists(filepath):
        os.remove(filepath)


# --- API Endpoints ---

@router.get("/health", tags=["root"])
async def health():
    """Health check endpoint."""
    return {"status": "ok", "message": "SlothTab is running"}


@router.get("/settings", tags=["settings"])
async def get_settings_endpoint():
    """Get current settings."""
    from .db import get_settings as db_get_settings
    return await db_get_settings()


@router.put("/settings", tags=["settings"])
async def put_settings_endpoint(key: str, value: str):
    """Set a setting value."""
    from .db import set_setting as db_set_setting
    return await db_set_setting(key, value)


@router.get("/files", tags=["files"])
async def list_files(
    path: str = "",
):
    """List files in a directory (within workspace)."""
    base = get_workspace_base()
    
    # If path is relative, resolve it within base
    if path:
        target = os.path.normpath(os.path.join(base, path))
    else:
        target = base
    
    # Security: ensure target is within base
    if not is_safe_path(base, target):
        raise HTTPException(status_code=400, detail="Path escapes workspace")
    
    if not os.path.isdir(target):
        return {"files": [], "folders": []}
    
    files = []
    folders = []
    
    for item in sorted(os.listdir(target)):
        item_path = os.path.join(target, item)
        file_info = get_file_info(item_path)
        
        if os.path.isdir(item_path):
            folders.append(
                {
                    "name": item,
                    "path": os.path.relpath(item_path, base),
                    "item_type": "folder",
                }
            )
        else:
            files.append(
                {
                    "name": item,
                    "path": os.path.relpath(item_path, base),
                    "item_type": "file",
                    "size": file_info.get("size", 0),
                    "extension": file_info.get("extension", ""),
                }
            )
    
    return {"files": files, "folders": folders}


@router.post("/files/analyze", tags=["files"])
async def analyze_file(
    file_path: str,
):
    """Analyze a single file using the AI provider."""
    base = get_workspace_base()
    
    # Resolve the file path
    if os.path.isabs(file_path):
        target = os.path.normpath(file_path)
    else:
        target = os.path.normpath(os.path.join(base, file_path))
    
    # Security check
    if not is_safe_path(base, target):
        raise HTTPException(status_code=400, detail="Path escapes workspace")
    
    if not os.path.exists(target):
        raise HTTPException(status_code=404, detail="File not found")
    
    # Get file info and processing
    file_info = get_file_info(target)
    
    # Extract text
    processor, proc_error = get_processor_for_file(target)
    
    extracted_text = ""
    if processor:
        extracted_text, proc_error = extract_text_from_pdf.__wrapped__(
            target
        ) if "pdf" in processor else (
            extract_text_from_docx.__wrapped__(target) if "docx" in processor else (
                extract_text_from_txt.__wrapped__(target) if "txt" in processor else (
                    extract_text_from_md.__wrapped__(target) if "md" in processor else (
                        extract_text_from_image.__wrapped__(target) if "image" in processor else ""
                    )
                )
            )
        )
    
    # If we have a provider, run AI analysis
    # Note: In a real app, we'd get the provider from settings
    # For now, we'll skip AI or use a placeholder
    
    # Store file in database
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if file already tracked
    cursor.execute("SELECT id FROM files WHERE original_path = ?", (target,))
    existing = cursor.fetchone()
    
    if existing:
        file_id = existing[0]
        # Update current_path if changed
        cursor.execute(
            "UPDATE files SET current_path = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (target, file_id),
        )
    else:
        cursor.execute(
            """
            INSERT INTO files (original_path, current_path, original_filename, current_filename, file_hash, file_type, file_size)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                target,
                target,
                os.path.basename(target),
                os.path.basename(target),
                file_info.get("hash", ""),
                file_info.get("extension", "") or "unknown",
                file_info.get("size", 0),
            ),
        )
        file_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    
    return {
        "file_id": file_id,
        "file_info": file_info,
        "extracted_text": extracted_text[:2000] if extracted_text else "",
        "proc_error": proc_error,
    }


@router.post("/files/analyze-all", tags=["files"])
async def analyze_all_files(
    folder_path: str,
    background_tasks: BackgroundTasks,
):
    """Analyze all files in a folder."""
    base = get_workspace_base()
    
    # Resolve folder path
    if os.path.isabs(folder_path):
        target = os.path.normpath(folder_path)
    else:
        target = os.path.normpath(os.path.join(base, folder_path))
    
    # Security check
    if not is_safe_path(base, target):
        raise HTTPException(status_code=400, detail="Path escapes workspace")
    
    if not os.path.isdir(target):
        raise HTTPException(status_code=404, detail="Folder not found")
    
    # Get all supported files
    supported_extensions = get_supported_extensions()
    files_to_process = []
    
    for root, dirs, files in os.walk(target):
        for fname in sorted(files):
            fpath = os.path.join(root, fname)
            ext = os.path.splitext(fname)[1].lower()
            if ext in supported_extensions:
                files_to_process.append(fpath)
    
    # Process each file
    results = []
    
    # Get AI provider from settings (placeholder - would use real settings)
    # provider = await get_ai_provider_from_settings()
    
    for fpath in files_to_process:
        result = await process_file_async(
            fpath,
            # ai_provider=provider,
            # analysis_prompt=FILE_CLASSIFICATION_PROMPT,
        )
        results.append(result)
    
    # Store all analyses in DB
    conn = get_connection()
    cursor = conn.cursor()
    
    for result in results:
        file_info = result.get("file_info", {})
        extracted_text = result.get("extracted_text", "")
        
        # Get file_id
        cursor.execute("SELECT id FROM files WHERE original_path = ?", (file_info.get("filepath", ""),))
        row = cursor.fetchone()
        file_id = row[0] if row else None
        
        if file_id and not result.get("process_error"):
            # Try AI analysis (skipped for now - placeholder)
            pass
    
    conn.commit()
    conn.close()
    
    return {
        "folder": folder_path,
        "total_files": len(files_to_process),
        "processed": len(results),
        "results": len(results),
    }


@router.post("/files/apply", tags=["operations"])
async def apply_analysis(
    file_id: int,
    suggested_filename: str,
    suggested_destination: str,
):
    """Apply a file organization suggestion after user approval."""
    from .db import get_connection
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get the file record
    cursor.execute("SELECT * FROM files WHERE id = ?", (file_id,))
    file_row = cursor.fetchone()
    
    if not file_row:
        conn.close()
        raise HTTPException(status_code=404, detail="File not found")
    
    original_path = file_row[2]  # original_path
    original_filename = file_row[3]  # original_filename
    current_path = file_row[4]  # current_path
    
    # Sanitize and validate the suggested filename
    safe_filename = sanitize_filename(suggested_filename)
    if not safe_filename:
        conn.close()
        raise HTTPException(status_code=400, detail="Invalid filename generated")
    
    # Ensure it has an extension
    ext = os.path.splitext(original_filename)[1]
    if ext and not safe_filename.lower().endswith(ext.lower()):
        safe_filename += ext
    
    # Validate destination is within workspace
    base = get_workspace_base()
    full_dest = os.path.normpath(os.path.join(base, suggested_destination))
    
    if not is_safe_path(base, full_dest):
        conn.close()
        raise HTTPException(status_code=400, detail="Destination escapes workspace")
    
    # Create full destination path
    dest_filename = safe_filename
    dest_path = os.path.join(full_dest, dest_filename)
    
    # Normalize current_path
    current_path_norm = os.path.normpath(current_path)
    
    # Perform the move operation
    try:
        # Move the file
        safe_os_rename(current_path, dest_path)
        
        # Update the database
        new_current_path = os.path.relpath(dest_path, base)
        
        cursor.execute(
            """
            UPDATE files 
            SET current_path = ?, current_filename = ?
            WHERE id = ?
        """,
            (new_current_path, safe_filename, file_id),
        )
        
        # Record the operation
        cursor.execute(
            """
            INSERT INTO operations (file_id, operation_type, old_path, new_path)
            VALUES (?, ?, ?, ?)
        """,
            (
                file_id,
                "move",
                current_path_norm,
                new_current_path,
            ),
        )
        
        conn.commit()
    except FileExistsError:
        conn.close()
        raise HTTPException(status_code=409, detail="Destination file already exists")
    except Exception as e:
        conn.rollback()
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))
    
    conn.close()
    
    return {
        "success": True,
        "message": f"File moved to {suggested_destination}/{safe_filename}",
        "original_path": original_path,
        "new_path": dest_path,
    }


@router.post("/files/undo", tags=["operations"])
async def undo_last_operation():
    """Undo the last file operation."""
    from .db import get_connection
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get the most recent undone operation
    cursor.execute(
        "SELECT id, file_id, operation_type, old_path, new_path FROM operations WHERE undone = 0 ORDER BY timestamp DESC LIMIT 1"
    )
    op_row = cursor.fetchone()
    
    if not op_row:
        conn.close()
        return {"success": True, "message": "No operations to undo"}
    
    op_id, file_id, op_type, old_path, new_path = op_row
    
    try:
        if op_type == "move":
            # Move back
            if os.path.exists(new_path):
                safe_os_rename(new_path, old_path)
        elif op_type == "rename":
            # Rename back
            if os.path.exists(new_path):
                safe_os_rename(new_path, old_path)
        
        # Mark operation as undone
        cursor.execute(
            "UPDATE operations SET undone = 1 WHERE id = ?",
            (op_id,),
        )
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    conn.close()
    
    return {"success": True, "message": "Operation undone"}


@router.get("/activity", tags=["activity"])
async def get_activity(
    filter: str = "all",
    limit: int = 50,
):
    """Get activity history."""
    from .db import get_connection
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Build filter query
    if filter == "all":
        cursor.execute(
            """
            SELECT o.id, f.current_filename, o.operation_type, o.old_path, o.new_path, o.timestamp
            FROM operations o
            JOIN files f ON o.file_id = f.id
            ORDER BY o.timestamp DESC
            LIMIT ?
        """,
            (limit,),
        )
    else:
        cursor.execute(
            """
            SELECT o.id, f.current_filename, o.operation_type, o.old_path, o.new_path, o.timestamp
            FROM operations o
            JOIN files f ON o.file_id = f.id
            WHERE o.operation_type = ?
            ORDER BY o.timestamp DESC
            LIMIT ?
        """,
            (filter, limit),
        )
    
    rows = cursor.fetchall()
    conn.close()
    
    activity = []
    for row in rows:
        activity.append(
            {
                "id": row[0],
                "filename": row[1],
                "operation": row[2],
                "old_path": row[3],
                "new_path": row[4],
                "timestamp": row[5],
            }
        )
    
    return {"activity": activity, "filter": filter}


@router.get("/rules", tags=["rules"])
async def get_rules():
    """Get all rules."""
    from .db import get_connection
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, conditions, actions, enabled FROM rules")
    rows = cursor.fetchall()
    conn.close()
    
    rules = []
    for row in rows:
        rules.append(
            {
                "id": row[0],
                "name": row[1],
                "conditions": row[2] or "",
                "actions": row[3] or "",
                "enabled": bool(row[4]),
            }
        )
    
    return {"rules": rules}


@router.post("/rules", tags=["rules"])
async def create_rule(
    name: str,
    conditions: str = "",
    actions: str = "",
    enabled: bool = True,
):
    """Create a new rule."""
    from .db import get_connection
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO rules (name, conditions, actions, enabled)
        VALUES (?, ?, ?, ?)
    """,
        (name, conditions, actions, 1 if enabled else 0),
    )
    conn.commit()
    conn.close()
    
    return {"id": cursor.lastrowid, "name": name, "enabled": enabled}


@router.post("/files/duplicate-check", tags=["files"])
async def check_duplicates(file_path: str):
    """Check a file for duplicates in the workspace."""
    base = get_workspace_base()
    
    # Resolve path
    if os.path.isabs(file_path):
        target = os.path.normpath(file_path)
    else:
        target = os.path.normpath(os.path.join(base, file_path))
    
    # Security check
    if not is_safe_path(base, target):
        raise HTTPException(status_code=400, detail="Path escapes workspace")
    
    if not os.path.exists(target):
        raise HTTPException(status_code=404, detail="File not found")
    
    file_hash = compute_file_hash(target)
    file_size = os.path.getsize(target)
    
    # Find files with same hash and size
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT original_path, current_filename, file_size FROM files WHERE file_hash = ? AND original_path != ?",
        (file_hash, target),
    )
    same_hash = cursor.fetchall()
    conn.close()
    
    similar_files = []
    for row in same_hash:
        similar_files.append(
            {
                "path": row[0],
                "filename": row[1],
                "size": row[2],
            }
        )
    
    is_exact_duplicate = len(similar_files) > 0
    
    return {
        "is_duplicate": is_exact_duplicate,
        "is_exact_duplicate": is_exact_duplicate,
        "confidence": 1.0 if is_exact_duplicate else 0.0,
        "similar_files": similar_files,
        "description": f"Found {len(similar_files)} file(s) with same hash" if is_exact_duplicate else "No exact duplicates found",
    }