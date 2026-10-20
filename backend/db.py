import sqlite3
import os
import json
from typing import Optional, Dict, Any

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
DB_PATH = os.path.join(DATA_DIR, "slothtab.db")


def get_db_path() -> str:
    return DB_PATH


def get_connection():
    """Get a database connection, creating tables if needed."""
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database with required tables."""
    conn = get_connection()
    cursor = conn.cursor()

    # files table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_path TEXT NOT NULL,
            current_path TEXT NOT NULL,
            original_filename TEXT NOT NULL,
            current_filename TEXT NOT NULL,
            file_hash TEXT,
            file_type TEXT,
            file_size INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # analyses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id INTEGER NOT NULL,
            category TEXT,
            subcategory TEXT,
            summary TEXT,
            suggested_filename TEXT,
            suggested_destination TEXT,
            importance TEXT,
            confidence REAL,
            tags TEXT,
            reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (file_id) REFERENCES files (id)
        )
    """)

    # operations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS operations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id INTEGER NOT NULL,
            operation_type TEXT NOT NULL,
            old_path TEXT,
            new_path TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            undone INTEGER DEFAULT 0,
            FOREIGN KEY (file_id) REFERENCES files (id)
        )
    """)

    # settings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # rules table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            conditions TEXT,
            actions TEXT,
            enabled INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ai_provider_settings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_provider_settings (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def get_settings() -> Dict[str, Any]:
    """Get all settings from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT key, value FROM settings")
    rows = cursor.fetchall()
    conn.close()
    return {row[0]: row[1] for row in rows}


async def get_settings_async() -> Dict[str, Any]:
    """Async wrapper around get_settings for use in async endpoints."""
    return get_settings()


def set_setting(key: str, value: str):
    """Set a setting value (upsert)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO settings (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = ?, updated_at = CURRENT_TIMESTAMP",
        (key, value, value),
    )
    conn.commit()
    conn.close()
    return {"key": key, "value": value}


async def set_setting_async(key: str, value: str):
    """Async wrapper around set_setting for use in async endpoints."""
    return set_setting(key, value)