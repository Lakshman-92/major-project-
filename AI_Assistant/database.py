"""SQLite database utilities for tasks and reminders."""

import sqlite3
from typing import Optional

from config import APP_CONFIG


def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Return a SQLite connection with foreign keys enabled."""

    connection = sqlite3.connect(db_path or APP_CONFIG.database_path)
    connection.execute("PRAGMA foreign_keys = ON;")
    return connection


def init_db() -> None:
    """Initialize the tasks table if it does not exist."""

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            task_date TEXT NOT NULL,
            task_time TEXT NOT NULL,
            priority TEXT NOT NULL,
            reminded INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    connection.commit()
    connection.close()
