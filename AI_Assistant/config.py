"""Configuration for the Agentic AI assistant project."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class EmailConfig:
    """Email settings for IMAP access."""

    imap_server: str = "imap.gmail.com"
    imap_port: int = 993
    email_address: str = "your_email@example.com"
    email_password: str = "your_app_password"
    important_senders: List[str] = field(
        default_factory=lambda: ["exam-office@example.com", "hr@example.com"]
    )
    important_keywords: List[str] = field(
        default_factory=lambda: [
            "exam",
            "deadline",
            "interview",
            "urgent",
            "payment",
        ]
    )


@dataclass
class AppConfig:
    """General application settings."""

    database_path: str = "assistant.db"
    use_dummy_emails: bool = True


EMAIL_CONFIG = EmailConfig()
APP_CONFIG = AppConfig()
