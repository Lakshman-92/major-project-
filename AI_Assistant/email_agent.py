"""Email fetching and important email detection logic."""

from __future__ import annotations

import imaplib
import email
from dataclasses import dataclass
from typing import Iterable, List

from config import EMAIL_CONFIG, APP_CONFIG


@dataclass
class EmailMessage:
    """Simple representation of an email message."""

    sender: str
    subject: str
    body: str
    is_unread: bool


class EmailAgent:
    """Handles email fetching and important email identification."""

    def __init__(self) -> None:
        self.config = EMAIL_CONFIG

    def fetch_emails(self) -> List[EmailMessage]:
        """Fetch emails from IMAP or return dummy data for local testing."""

        if APP_CONFIG.use_dummy_emails:
            return self._dummy_emails()
        return self._fetch_from_imap()

    def identify_important(self, emails: Iterable[EmailMessage]) -> List[EmailMessage]:
        """Filter emails based on sender, keywords, and unread status."""

        important = []
        for message in emails:
            if self._is_important(message):
                important.append(message)
        return important

    def _is_important(self, message: EmailMessage) -> bool:
        """Determine if a single email is important."""

        sender_match = any(
            sender.lower() in message.sender.lower()
            for sender in self.config.important_senders
        )
        keyword_match = any(
            keyword.lower() in f"{message.subject} {message.body}".lower()
            for keyword in self.config.important_keywords
        )
        return message.is_unread and (sender_match or keyword_match)

    def _fetch_from_imap(self) -> List[EmailMessage]:
        """Fetch emails using IMAP (Gmail app password required)."""

        messages: List[EmailMessage] = []
        with imaplib.IMAP4_SSL(self.config.imap_server, self.config.imap_port) as mail:
            mail.login(self.config.email_address, self.config.email_password)
            mail.select("INBOX")
            status, data = mail.search(None, "ALL")
            if status != "OK":
                return messages
            for num in data[0].split()[-10:]:
                status, msg_data = mail.fetch(num, "(RFC822)")
                if status != "OK":
                    continue
                raw = msg_data[0][1]
                msg = email.message_from_bytes(raw)
                subject = msg.get("Subject", "")
                sender = msg.get("From", "")
                is_unread = "\\Seen" not in msg.get("Flags", "")
                body = self._extract_body(msg)
                messages.append(
                    EmailMessage(
                        sender=sender,
                        subject=subject,
                        body=body,
                        is_unread=is_unread,
                    )
                )
        return messages

    @staticmethod
    def _extract_body(message: email.message.Message) -> str:
        """Extract text body from a MIME email message."""

        if message.is_multipart():
            for part in message.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode(errors="ignore")
        payload = message.get_payload(decode=True)
        return payload.decode(errors="ignore") if payload else ""

    @staticmethod
    def _dummy_emails() -> List[EmailMessage]:
        """Provide dummy emails for demo purposes."""

        return [
            EmailMessage(
                sender="exam-office@example.com",
                subject="Exam deadline reminder",
                body="Your exam registration deadline is tomorrow.",
                is_unread=True,
            ),
            EmailMessage(
                sender="friend@example.com",
                subject="Weekend plans",
                body="Let's catch up soon.",
                is_unread=True,
            ),
            EmailMessage(
                sender="hr@example.com",
                subject="Interview schedule",
                body="Your interview is scheduled for next week.",
                is_unread=False,
            ),
        ]
