"""Comprehensive email notification service for QuickTym."""

import asyncio
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

from app.core.config import settings
from app.services.email_templates import EmailTemplates

logger = logging.getLogger(__name__)


class NotificationService:
    """Comprehensive notification service for all events."""
    
    def __init__(self):
        self.backend = settings.EMAIL_BACKEND
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.smtp_from_email = settings.SMTP_FROM_EMAIL
        self.smtp_use_tls = settings.SMTP_USE_TLS
        self.templates = EmailTemplates()
    
    async def _create_message(
        self,
        to_email: str,
        subject: str,
        html_body: str,
        text_body: Optional[str] = None,
        attachments: Optional[List[Dict[str, Any]]] = None
    ) -> MIMEMultipart:
        """Create an email message with HTML and text versions."""
        message = MIMEMultipart("alternative")
        message["From"] = self.smtp_from_email
        message["To"] = to_email
        message["Subject"] = subject
        message["Date"] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")
        
        # Add text version
        if text_body:
            message.attach(MIMEText(text_body, "plain"))
        
        # Add HTML version
        message.attach(MIMEText(html_body, "html"))
        
        # Add attachments
        if attachments:
            for attachment in attachments:
                part = MIMEApplication(
                    attachment["content"],
                    Name=attachment["filename"]
                )
                part["Content-Disposition"] = f'attachment; filename="{attachment["filename"]}"'
                message.attach(part)
        
        return message
    
    async def _send_smtp_email(self, message: MIMEMultipart) -> bool:
        """Send email via SMTP asynchronously."""
        try:
            await aiosmtplib.send(
                message,
                hostname=self.smtp_host,
                port=self.smtp_port,
                username=self.smtp_user,
                password=self.smtp_password,
                use_tls=self.smtp_use_tls
            )
            logger.info(f"Email sent successfully to {message['To']}")
            return True
        except Exception as e:
            logger.error(f"SMTP Email error: {e}")
            return False
    
    def _send_console_email(self, message: MIMEMultipart) -> bool:
        """Send email to console (for development/testing)."""
        print(f"\n{'='*60}")
        print(f"[EMAIL] To: {message['To']}")
        print(f"[EMAIL] Subject: {message['Subject']}")
        print(f"[EMAIL] Date: {message['Date']}")
        print(f"{'='*60}")
        print(message.as_string())
        print(f"{'='*60}\n")
        return True
    
    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_body: str,
        text_body: Optional[str] = None,
        attachments: Optional[List[Dict[str, Any]]] = None
    ) -> bool:
        """Send email with given content."""
        message = await self._create_message(to_email, subject, html_body, text_body, attachments)
        
        if self.backend == "console":
            return self._send_console_email(message)
        else:
            return await self._send_smtp_email(message)
    
    # ==================== USER NOTIFICATIONS ====================
    
    async def send_registration_welcome(
        self,
        user_email: str,
        user_name: str
    ) -> bool:
        """Send welcome email to newly registered user."""
        template = self.templates.registration_welcome(user_name, user_email)
        return await self.send_email(
            to_email=user_email,
            subject=template["subject"],
            html_body=template["html"],
            text_body=template["text"]
        )
    
    async def send_password_reset(
        self,
        user_email: str,
        reset_token: str,
        reset_url: str
    ) -> bool:
        """Send password reset email."""
        subject = "Reset Your Password - QuickTym"
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2>Reset Your Password</h2>
            <p>You requested to reset your password. Click the link below:</p>
            <a href="{reset_url}?token={reset_token}&email={user_email}" 
               style="background-color: #4F46E5; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                Reset Password
            </a>
            <p>This link will expire in 1 hour.</p>
            <p>If you didn't request this, please ignore this email.</p>
        </body>
        </html>
        """
        text_body = f"Reset your password at: {reset_url}?token={reset_token}&email={user_email}"
        
        return await self.send_email(user_email, subject, html_body, text_body)
    
    # ==================== RENTAL NOTIFICATIONS ====================
    
    async def send_rental_confirmation(
        self,
        user_email: str,
        user_name: str,
        rental_id: str,
        product_name: str,
        start_time: str,
        hourly_rate: float,
        delivery_address: str
    ) -> bool:
        """Send rental confirmation email."""
        template = self.templates.rental_confirmation(
            user_name, rental_id, product_name, start_time, hourly_rate, delivery_address
        )
        return await self.send_email(
            to_email=user_email,
            subject=template["subject"],
            html_body=template["html"],
            text_body=template["text"]
        )
    
    async def send_rental_cancellation(
        self,
        user_email: str,
        user_name: str,
        rental_id: str,
        product_name: str,
        reason: Optional[str] = None
    ) -> bool:
        """Send rental cancellation email."""
        subject = f"Rental Cancelled: {product_name}"
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2>Rental Cancelled</h2>
            <p>Hi {user_name},</p>
            <p>Your rental for <strong>{product_name}</strong> has been cancelled.</p>
            <p><strong>Rental ID:</strong> {rental_id}</p>
            {f'<p><strong>Reason:</strong> {reason}</p>' if reason else ''}
            <p>If you have any questions, please contact our support team.</p>
        </body>
        </html>
        """
        text_body = f"Rental {rental_id} for {product_name} has been cancelled."
        
        return await self.send_email(user_email, subject, html_body, text_body)
    
    async def send_rental_completed(
        self,
        user_email: str,
        user_name: str,
        rental_id: str,
        product_name: str,
        total_duration: str,
        total_amount: float,
        payment_status: str
    ) -> bool:
        """Send rental completion email."""
        template = self.templates.rental_completed(
            user_name, rental_id, product_name, total_duration, total_amount, payment_status
        )
        return await self.send_email(
            to_email=user_email,
            subject=template["subject"],
            html_body=template["html"],
            text_body=template["text"]
        )
    
    # ==================== DELIVERY NOTIFICATIONS ====================
    
    async def send_delivery_update(
        self,
        user_email: str,
        user_name: str,
        rental_id: str,
        product_name: str,
        status: str,
        delivery_partner_name: str,
        delivery_partner_phone: str,
        estimated_time: Optional[str] = None
    ) -> bool:
        """Send delivery status update email."""
        template = self.templates.delivery_update(
            user_name, rental_id, product_name, status,
            delivery_partner_name, delivery_partner_phone, estimated_time
        )
        return await self.send_email(
            to_email=user_email,
            subject=template["subject"],
            html_body=template["html"],
            text_body=template["text"]
        )
    
    async def send_pickup_reminder(
        self,
        user_email: str,
        user_name: str,
        rental_id: str,
        product_name: str,
        duration_hours: float,
        current_cost: float
    ) -> bool:
        """Send pickup reminder email."""
        template = self.templates.pickup_reminder(
            user_name, rental_id, product_name, duration_hours, current_cost
        )
        return await self.send_email(
            to_email=user_email,
            subject=template["subject"],
            html_body=template["html"],
            text_body=template["text"]
        )
    
    # ==================== PAYMENT NOTIFICATIONS ====================
    
    async def send_payment_success(
        self,
        user_email: str,
        user_name: str,
        rental_id: str,
        amount: float,
        transaction_id: str,
        payment_method: str,
        invoice_pdf: Optional[bytes] = None
    ) -> bool:
        """Send payment success email with optional invoice attachment."""
        template = self.templates.payment_success(
            user_name, rental_id, amount, transaction_id, payment_method
        )
        
        attachments = None
        if invoice_pdf:
            attachments = [{
                "filename": f"invoice_{rental_id}.pdf",
                "content": invoice_pdf
            }]
        
        return await self.send_email(
            to_email=user_email,
            subject=template["subject"],
            html_body=template["html"],
            text_body=template["text"],
            attachments=attachments
        )
    
    async def send_payment_failure(
        self,
        user_email: str,
        user_name: str,
        rental_id: str,
        amount: float,
        failure_reason: str
    ) -> bool:
        """Send payment failure notification."""
        subject = f"Payment Failed - ₹{amount}"
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2>Payment Failed</h2>
            <p>Hi {user_name},</p>
            <p>Unfortunately, your payment of <strong>₹{amount}</strong> could not be processed.</p>
            <p><strong>Reason:</strong> {failure_reason}</p>
            <p><strong>Rental ID:</strong> {rental_id}</p>
            <p>Please try again with a different payment method.</p>
            <a href="https://quicktym.com/rentals/{rental_id}/pay" 
               style="background-color: #4F46E5; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                Retry Payment
            </a>
        </body>
        </html>
        """
        text_body = f"Payment of ₹{amount} failed. Reason: {failure_reason}. Please retry."
        
        return await self.send_email(user_email, subject, html_body, text_body)
    
    async def send_refund_processed(
        self,
        user_email: str,
        user_name: str,
        rental_id: str,
        refund_amount: float,
        refund_id: str
    ) -> bool:
        """Send refund confirmation email."""
        subject = f"Refund Processed - ₹{refund_amount}"
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2>Refund Processed</h2>
            <p>Hi {user_name},</p>
            <p>Your refund of <strong>₹{refund_amount}</strong> has been processed successfully.</p>
            <p><strong>Refund ID:</strong> {refund_id}</p>
            <p><strong>Rental ID:</strong> {rental_id}</p>
            <p>The refund will be credited to your original payment method within 5-7 business days.</p>
        </body>
        </html>
        """
        text_body = f"Refund of ₹{refund_amount} processed. ID: {refund_id}"
        
        return await self.send_email(user_email, subject, html_body, text_body)
    
    # ==================== DELIVERY PARTNER NOTIFICATIONS ====================
    
    async def send_delivery_partner_assignment(
        self,
        partner_email: str,
        partner_name: str,
        delivery_id: str,
        product_name: str,
        customer_name: str,
        pickup_address: str,
        delivery_address: str,
        contact_phone: str
    ) -> bool:
        """Send delivery assignment to delivery partner."""
        template = self.templates.delivery_partner_assignment(
            partner_name, delivery_id, product_name, customer_name,
            pickup_address, delivery_address, contact_phone
        )
        return await self.send_email(
            to_email=partner_email,
            subject=template["subject"],
            html_body=template["html"],
            text_body=template["text"]
        )
    
    # ==================== REVIEW NOTIFICATIONS ====================
    
    async def send_review_request(
        self,
        user_email: str,
        user_name: str,
        rental_id: str,
        product_name: str
    ) -> bool:
        """Send review request email."""
        template = self.templates.review_request(user_name, rental_id, product_name)
        return await self.send_email(
            to_email=user_email,
            subject=template["subject"],
            html_body=template["html"],
            text_body=template["text"]
        )
    
    # ==================== ADMIN NOTIFICATIONS ====================
    
    async def send_admin_alert(
        self,
        admin_email: str,
        alert_type: str,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Send admin alert notification."""
        subject = f"[ALERT] {alert_type} - QuickTym"
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2>Admin Alert: {alert_type}</h2>
            <p>{message}</p>
            {f'<pre>{details}</pre>' if details else ''}
            <p>Time: {datetime.now().isoformat()}</p>
        </body>
        </html>
        """
        text_body = f"Alert: {alert_type} - {message}"
        
        return await self.send_email(admin_email, subject, html_body, text_body)


# Singleton instance
notification_service = NotificationService()
