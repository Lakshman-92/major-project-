"""Display utilities for tasks and reminders."""

from typing import List, Dict


def display_tasks(title: str, tasks: List[Dict[str, str]]) -> None:
    """Pretty-print a list of tasks."""

    print(f"\n=== {title} ===")
    if not tasks:
        print("No tasks available.")
        return
    for task in tasks:
        print(
            f"#{task['id']} | {task['task_date']} {task['task_time']} | "
            f"{task['priority']} | {task['title']}"
        )


def display_reminder(task: Dict[str, str]) -> None:
    """Display a clear reminder message for a task."""

    print(
        "\n!!! REMINDER !!!\n"
        f"Task: {task['title']}\n"
        f"When: {task['task_date']} {task['task_time']}\n"
        f"Priority: {task['priority']}\n"
        "=================\n"
    )
