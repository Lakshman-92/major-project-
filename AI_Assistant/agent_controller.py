"""Agentic AI controller that plans actions based on user intent."""

from __future__ import annotations

from typing import Dict

from display import display_tasks
from email_agent import EmailAgent
from reminder_agent import ReminderAgent
from task_manager import TaskManager


class AgentController:
    """Rule-based agent that routes user requests to tools."""

    def __init__(self) -> None:
        self.email_agent = EmailAgent()
        self.task_manager = TaskManager()
        self.reminder_agent = ReminderAgent(self.task_manager)

    def handle_input(self, user_input: str) -> None:
        """Interpret input, plan actions, and call the right tools."""

        intent = self._detect_intent(user_input)

        # Agentic planning: choose a sequence of tool calls based on intent.
        if intent == "check_email":
            self._check_emails()
        elif intent == "add_task":
            self._add_task_from_input(user_input)
        elif intent == "show_tasks":
            self._show_tasks()
        elif intent == "start_reminders":
            print("Reminder agent started in background.")
            self.reminder_agent.start()
        else:
            print("I can help with: check email, add task, show tasks, start reminders.")

    def _detect_intent(self, user_input: str) -> str:
        """Simple rule-based intent detection."""

        text = user_input.lower()
        if "check" in text and "email" in text:
            return "check_email"
        if "add" in text and "task" in text:
            return "add_task"
        if "show" in text and "task" in text:
            return "show_tasks"
        if "start" in text and "reminder" in text:
            return "start_reminders"
        return "unknown"

    def _check_emails(self) -> None:
        """Fetch and notify about important emails."""

        emails = self.email_agent.fetch_emails()
        important_emails = self.email_agent.identify_important(emails)
        if not important_emails:
            print("No important emails found.")
            return
        print("Important emails detected:")
        for message in important_emails:
            print(f"- {message.subject} from {message.sender}")

    def _add_task_from_input(self, user_input: str) -> None:
        """Parse task details from input and add to database."""

        details = self._parse_key_values(user_input)
        title = details.get("title", "Untitled Task")
        task_date = details.get("date", "2099-12-31")
        task_time = details.get("time", "09:00")
        priority = details.get("priority", "Medium")
        task_id = self.task_manager.add_task(title, task_date, task_time, priority)
        print(f"Task added with ID: {task_id}")

    def _show_tasks(self) -> None:
        """Display today's and upcoming tasks."""

        grouped = self.task_manager.get_today_and_upcoming()
        display_tasks("Today's Tasks", grouped["today"])
        display_tasks("Upcoming Tasks", grouped["upcoming"])

    @staticmethod
    def _parse_key_values(text: str) -> Dict[str, str]:
        """Extract key=value pairs from user input."""

        parts = text.split()
        data: Dict[str, str] = {}
        for part in parts:
            if "=" in part:
                key, value = part.split("=", 1)
                data[key.strip().lower()] = value.strip()
        return data
