"""Task management logic using SQLite."""

from __future__ import annotations

import datetime as dt
from typing import List, Dict

from database import get_connection


class TaskManager:
    """Handles task creation and retrieval."""

    def add_task(self, title: str, task_date: str, task_time: str, priority: str) -> int:
        """Add a new task to the database and return its ID."""

        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO tasks (title, task_date, task_time, priority)
            VALUES (?, ?, ?, ?)
            """,
            (title, task_date, task_time, priority),
        )
        connection.commit()
        task_id = cursor.lastrowid
        connection.close()
        return int(task_id)

    def get_tasks(self) -> List[Dict[str, str]]:
        """Fetch all tasks sorted by date and time."""

        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id, title, task_date, task_time, priority, reminded
            FROM tasks
            ORDER BY task_date, task_time
            """
        )
        rows = cursor.fetchall()
        connection.close()
        return [
            {
                "id": row[0],
                "title": row[1],
                "task_date": row[2],
                "task_time": row[3],
                "priority": row[4],
                "reminded": row[5],
            }
            for row in rows
        ]

    def get_today_and_upcoming(self) -> Dict[str, List[Dict[str, str]]]:
        """Return tasks grouped into today and upcoming."""

        all_tasks = self.get_tasks()
        today_str = dt.date.today().isoformat()
        today_tasks = [task for task in all_tasks if task["task_date"] == today_str]
        upcoming_tasks = [
            task for task in all_tasks if task["task_date"] > today_str
        ]
        return {"today": today_tasks, "upcoming": upcoming_tasks}

    def mark_reminded(self, task_id: int) -> None:
        """Mark a task as reminded to avoid duplicate notifications."""

        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE tasks SET reminded = 1 WHERE id = ?", (task_id,))
        connection.commit()
        connection.close()
