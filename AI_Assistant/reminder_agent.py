"""Background reminder scheduler."""

from __future__ import annotations

import datetime as dt
import threading
import time
from typing import Optional

import schedule

from display import display_reminder
from task_manager import TaskManager


class ReminderAgent:
    """Checks tasks every minute and triggers reminders."""

    def __init__(self, task_manager: Optional[TaskManager] = None) -> None:
        self.task_manager = task_manager or TaskManager()
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def start(self) -> None:
        """Start the background scheduler."""

        schedule.clear()
        schedule.every(1).minutes.do(self.check_reminders)
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Stop the background scheduler."""

        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=2)

    def _run_loop(self) -> None:
        """Internal loop that runs scheduled jobs."""

        while not self._stop_event.is_set():
            schedule.run_pending()
            time.sleep(1)

    def check_reminders(self) -> None:
        """Check for tasks that should trigger reminders now."""

        now = dt.datetime.now()
        for task in self.task_manager.get_tasks():
            if task["reminded"]:
                continue
            task_dt = dt.datetime.fromisoformat(
                f"{task['task_date']} {task['task_time']}"
            )
            if task_dt <= now:
                display_reminder(task)
                self.task_manager.mark_reminded(task["id"])
