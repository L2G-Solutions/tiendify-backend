from app.config.config import settings
from app.config.mail_templates import MailTemplates
from app.services.mail_sender import MailSender


def build_database_url(host: str, username: str, password: str) -> str:
    return f"postgresql://{username}:{password}@{host}"


def send_store_created_email(user_name: str, user_email: str, store_name: str):
    """Sends welcome email to the user after shop cloud resources provisioning.

    Args:
        user_name (str): User's name
        user_email (str): User's email
        store_name (str): Store name

    Raises:
        Exception: Failed to send email
    """
    mail_templates = MailTemplates()
    mail_sender = MailSender()
    mail_content = mail_templates.render_store_created_template(user_name, store_name)

    status_code = mail_sender.send(
        subject="Tiendify - Your Store is Ready to Go!",
        recipients=user_email,
        body=mail_content,
        email_from=settings.EMAIL_SERVICE_FROM_EMAIL,
    )

    if not str(status_code).startswith("2"):
        raise Exception(f"Failed to send email. Status code: {status_code}")

    return True
