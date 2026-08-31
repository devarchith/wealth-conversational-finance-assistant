from abc import ABC, abstractmethod
from email.message import EmailMessage
import smtplib


class EmailProvider(ABC):
    name: str

    @abstractmethod
    def send(self, recipient: str, subject: str, body: str) -> str: ...


class MockEmailProvider(EmailProvider):
    name = "mock"

    def __init__(self) -> None:
        self.outbox: list[dict[str, str]] = []

    def send(self, recipient: str, subject: str, body: str) -> str:
        message_id = f"mock-{len(self.outbox) + 1}"
        self.outbox.append({"id": message_id, "recipient": recipient, "subject": subject, "body": body})
        return message_id


class SMTPEmailProvider(EmailProvider):
    name = "smtp"

    def __init__(self, host: str, port: int, username: str, password: str, from_email: str) -> None:
        self.host, self.port, self.username, self.password, self.from_email = host, port, username, password, from_email

    def send(self, recipient: str, subject: str, body: str) -> str:
        message = EmailMessage()
        message["From"], message["To"], message["Subject"] = self.from_email, recipient, subject
        message.set_content(body)
        with smtplib.SMTP(self.host, self.port, timeout=15) as smtp:
            smtp.starttls()
            smtp.login(self.username, self.password)
            smtp.send_message(message)
        return str(message.get("Message-ID") or "smtp-accepted")

