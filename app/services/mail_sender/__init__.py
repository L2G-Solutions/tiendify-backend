import logging
from typing import Any, List, Optional, Union

from email_validator import EmailNotValidError, validate_email
from python_http_client import InternalServerError, TooManyRequestsError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Attachment,
    Disposition,
    FileContent,
    FileName,
    FileType,
    Mail,
)
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config.config import settings

logger = logging.getLogger(__name__)


class MailSender:
    """Service class to send emails using SendGrid API."""

    def __init__(self):
        self.email_service = SendGridAPIClient(settings.EMAIL_SERVICE_API_KEY)

    def _validate_recipients(self, recipients: Union[str, List[str]]) -> List[str]:
        if isinstance(recipients, str):
            recipients = [recipients]
        for email in recipients:
            try:
                validate_email(email)
            except EmailNotValidError as e:
                logger.error(f"Invalid email address: {email}. Error: {e}")
                raise ValueError(f"Invalid email address: {email}")
        return recipients

    def _create_email_message(
        self,
        subject: str,
        body: Any,
        recipients: List[str],
        email_from: str,
        attachments: Optional[List[Attachment]] = None,
    ) -> Mail:
        email_message = Mail(
            from_email=email_from,
            to_emails=recipients,
            subject=subject,
            html_content=body,
        )
        if attachments:
            for attachment in attachments:
                email_message.add_attachment(attachment)
        return email_message

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True,
    )
    def send(
        self,
        subject: str,
        body: Any,
        recipients: Union[str, List[str]],
        email_from: str = settings.EMAIL_SERVICE_FROM_EMAIL,
        attachments: Optional[List[Attachment]] = None,
    ) -> int:
        recipients = self._validate_recipients(recipients)
        email_message = self._create_email_message(
            subject, body, recipients, email_from, attachments
        )

        try:
            response = self.email_service.send(email_message)
            return response.status_code
        except TooManyRequestsError as e:
            logger.error("SendGrid rate limit exceeded.")
            raise e
        except InternalServerError as e:
            logger.error("SendGrid internal server error.")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error sending email: {e}")
            raise

    @staticmethod
    def create_attachment(
        file_content: bytes, file_name: str, file_type: str
    ) -> Attachment:
        return Attachment(
            FileContent(file_content),
            FileName(file_name),
            FileType(file_type),
            Disposition("attachment"),
        )
