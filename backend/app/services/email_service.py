"""Email service for sending password reset emails."""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

from app.core.config import settings


class EmailService:
    """Email service for sending notifications."""
    
    def __init__(self):
        self.backend = settings.EMAIL_BACKEND
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.smtp_from_email = settings.SMTP_FROM_EMAIL
        self.smtp_use_tls = settings.SMTP_USE_TLS
    
    def _create_message(self, to_email: str, subject: str, body: str) -> MIMEMultipart:
        """Create an email message."""
        message = MIMEMultipart()
        message["From"] = self.smtp_from_email
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))
        return message
    
    def _send_smtp_email(self, message: MIMEMultipart) -> bool:
        """Send email via SMTP."""
        try:
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            if self.smtp_use_tls:
                server.starttls()
            if self.smtp_user and self.smtp_password:
                server.login(self.smtp_user, self.smtp_password)
            server.sendmail(self.smtp_from_email, message["To"], message.as_string())
            server.quit()
            return True
        except Exception as e:
            print(f"SMTP Email error: {e}")
            return False
    
    def _send_console_email(self, message: MIMEMultipart) -> bool:
        """Send email to console (for development/testing)."""
        print(f"\n{'='*50}")
        print(f"[EMAIL] To: {message['To']}")
        print(f"[EMAIL] Subject: {message['Subject']}")
        print(f"[EMAIL] Body:\n{message.as_string()}")
        print(f"{'='*50}\n")
        return True
    
    def send_password_reset_email(self, to_email: str, reset_token: str) -> bool:
        """Send password reset email to user."""
        reset_link = f"{settings.SMTP_FROM_EMAIL.split('@')[1]}/reset-password?token={reset_token}&email={to_email}"
        
        if self.backend == "console":
            print(f"[FORGOT_PASSWORD] Reset token for {to_email}: {reset_token}")
            print(f"[FORGOT_PASSWORD] Reset link: {reset_link}")
            print(f"[FORGOT_PASSWORD] User would receive email with reset link")
            return True
        
        body = f"""Hello,

You have requested to reset your password. Click the link below to reset your password:

{reset_link}

This link will expire in 1 hour.

If you didn't request a password reset, please ignore this email.

Best regards,
Quick Tym Team
"""
        
        message = self._create_message(to_email, "Reset Your Quick Tym Password", body)
        
        if self.backend == "smtp":
            return self._send_smtp_email(message)
        else:
            return self._send_console_email(message)


# Singleton instance
email_service = EmailService()