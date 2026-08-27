import os
import smtplib
from email.message import EmailMessage

def send_welcome_email(to_email:str, first_name: str):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    email_from = os.getenv("EMAIL_FROM")

    if not all([
        smtp_host,
        smtp_username,
        smtp_password,
        email_from,
    ]):
        raise ValueError("SMTP configuration is missing")

    message = EmailMessage()

    message["Subject"] = "Welcome to ShopSphere 🎉"
    message["From"] = email_from
    message["To"] = to_email

    message.set_content(
            f"""
    Hello {first_name},

    Welcome to ShopSphere!

    Your account has been successfully created.

    We are happy to have you with us.

    Regards,
    ShopSphere Team
    """
        )
    
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(message)