"""Email templates for various notification types."""

from datetime import datetime
from typing import Dict, Any, Optional


class EmailTemplates:
    """Email template generator for all notification types."""
    
    @staticmethod
    def get_base_template(title: str, content: str, action_url: Optional[str] = None, action_text: Optional[str] = None) -> str:
        """Get base HTML email template."""
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f4f4f4;
        }}
        .container {{
            background-color: #ffffff;
            border-radius: 10px;
            padding: 40px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            border-bottom: 3px solid #4F46E5;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .logo {{
            font-size: 32px;
            font-weight: bold;
            color: #4F46E5;
        }}
        .content {{
            margin-bottom: 30px;
        }}
        .button {{
            display: inline-block;
            padding: 12px 30px;
            background-color: #4F46E5;
            color: #ffffff;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            margin-top: 20px;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #e5e5e5;
            font-size: 12px;
            color: #666;
        }}
        .highlight {{
            background-color: #f0f9ff;
            padding: 15px;
            border-left: 4px solid #4F46E5;
            margin: 20px 0;
        }}
        .success {{
            background-color: #f0fdf4;
            border-left-color: #10B981;
        }}
        .warning {{
            background-color: #fef3c7;
            border-left-color: #F59E0B;
        }}
        .info {{
            background-color: #eff6ff;
            border-left-color: #3B82F6;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">⚡ QuickTym</div>
        </div>
        <div class="content">
            {content}
            {f'<a href="{action_url}" class="button">{action_text}</a>' if action_url and action_text else ''}
        </div>
        <div class="footer">
            <p>© {datetime.now().year} QuickTym Rentals. All rights reserved.</p>
            <p>Need help? Contact us at support@quicktym.com</p>
        </div>
    </div>
</body>
</html>
        """
    
    @staticmethod
    def registration_welcome(user_name: str, email: str) -> Dict[str, str]:
        """Welcome email for new user registration."""
        subject = "Welcome to QuickTym! 🎉"
        content = f"""
            <h2>Welcome to QuickTym, {user_name}!</h2>
            <p>Thank you for creating an account with QuickTym. You're now part of India's fastest-growing rental platform!</p>
            
            <div class="highlight success">
                <strong>Your account is ready!</strong><br>
                Email: {email}<br>
                Start exploring thousands of products available for rent.
            </div>
            
            <h3>What you can do now:</h3>
            <ul>
                <li>🏠 Browse products in your area</li>
                <li>⚡ Book rentals in just 3 clicks</li>
                <li>🚚 Get instant delivery</li>
                <li>💳 Pay only for the time you use</li>
            </ul>
        """
        
        return {
            "subject": subject,
            "html": EmailTemplates.get_base_template(
                title=subject,
                content=content,
                action_url="https://quicktym.com/browse",
                action_text="Start Browsing"
            ),
            "text": f"Welcome to QuickTym, {user_name}! Your account is ready. Start exploring products at quicktym.com"
        }
    
    @staticmethod
    def rental_confirmation(
        user_name: str,
        rental_id: str,
        product_name: str,
        start_time: str,
        hourly_rate: float,
        delivery_address: str
    ) -> Dict[str, str]:
        """Rental confirmation email."""
        subject = f"Rental Confirmed: {product_name} ⚡"
        content = f"""
            <h2>Your Rental is Confirmed!</h2>
            <p>Hi {user_name},</p>
            <p>Great news! Your rental has been successfully booked.</p>
            
            <div class="highlight">
                <strong>Rental Details:</strong><br>
                <strong>Product:</strong> {product_name}<br>
                <strong>Rental ID:</strong> {rental_id}<br>
                <strong>Start Time:</strong> {start_time}<br>
                <strong>Hourly Rate:</strong> ₹{hourly_rate}/hr<br>
                <strong>Delivery Address:</strong> {delivery_address}
            </div>
            
            <p>Our delivery partner will contact you shortly with an estimated delivery time.</p>
            
            <h3>What's Next?</h3>
            <ol>
                <li>Wait for delivery partner confirmation</li>
                <li>Receive your product at the scheduled time</li>
                <li>Start using your rental</li>
                <li>Request pickup when done</li>
            </ol>
        """
        
        return {
            "subject": subject,
            "html": EmailTemplates.get_base_template(
                title=subject,
                content=content,
                action_url=f"https://quicktym.com/rentals/{rental_id}",
                action_text="Track Your Rental"
            ),
            "text": f"Rental confirmed! Product: {product_name}, ID: {rental_id}, Start: {start_time}"
        }
    
    @staticmethod
    def delivery_update(
        user_name: str,
        rental_id: str,
        product_name: str,
        status: str,
        delivery_partner_name: str,
        delivery_partner_phone: str,
        estimated_time: Optional[str] = None
    ) -> Dict[str, str]:
        """Delivery status update email."""
        subject = f"Delivery Update: {product_name} 🚚"
        content = f"""
            <h2>Delivery Status Update</h2>
            <p>Hi {user_name},</p>
            
            <div class="highlight info">
                <strong>Status:</strong> {status.upper()}<br>
                <strong>Product:</strong> {product_name}<br>
                {f'<strong>Estimated Arrival:</strong> {estimated_time}<br>' if estimated_time else ''}
            </div>
            
            <div class="highlight">
                <strong>Delivery Partner:</strong><br>
                Name: {delivery_partner_name}<br>
                Phone: {delivery_partner_phone}<br>
            </div>
            
            <p>Your delivery partner will contact you when they're nearby. Please keep your phone handy!</p>
        """
        
        return {
            "subject": subject,
            "html": EmailTemplates.get_base_template(
                title=subject,
                content=content,
                action_url=f"https://quicktym.com/rentals/{rental_id}",
                action_text="Track Live Location"
            ),
            "text": f"Delivery update for {product_name}: Status {status}. Partner: {delivery_partner_name} ({delivery_partner_phone})"
        }
    
    @staticmethod
    def payment_success(
        user_name: str,
        rental_id: str,
        amount: float,
        transaction_id: str,
        payment_method: str
    ) -> Dict[str, str]:
        """Payment success email with invoice."""
        subject = f"Payment Successful - ₹{amount} ✅"
        content = f"""
            <h2>Payment Successful!</h2>
            <p>Hi {user_name},</p>
            <p>Your payment has been successfully processed.</p>
            
            <div class="highlight success">
                <strong>Payment Details:</strong><br>
                <strong>Amount:</strong> ₹{amount}<br>
                <strong>Transaction ID:</strong> {transaction_id}<br>
                <strong>Payment Method:</strong> {payment_method.upper()}<br>
                <strong>Rental ID:</strong> {rental_id}<br>
            </div>
            
            <p>Thank you for using QuickTym! Your invoice is attached to this email.</p>
        """
        
        return {
            "subject": subject,
            "html": EmailTemplates.get_base_template(
                title=subject,
                content=content,
                action_url=f"https://quicktym.com/rentals/{rental_id}/invoice",
                action_text="Download Invoice"
            ),
            "text": f"Payment of ₹{amount} successful. Transaction ID: {transaction_id}"
        }
    
    @staticmethod
    def pickup_reminder(
        user_name: str,
        rental_id: str,
        product_name: str,
        duration_hours: float,
        current_cost: float
    ) -> Dict[str, str]:
        """Pickup reminder email."""
        subject = f"Time to Return: {product_name} ⏰"
        content = f"""
            <h2>Ready for Pickup?</h2>
            <p>Hi {user_name},</p>
            <p>Your rental has been active for <strong>{duration_hours:.1f} hours</strong>.</p>
            
            <div class="highlight warning">
                <strong>Current Cost:</strong> ₹{current_cost:.2f}<br>
                <strong>Product:</strong> {product_name}<br>
                <strong>Rental ID:</strong> {rental_id}<br>
            </div>
            
            <p>When you're done using the product, click below to request a pickup. Our delivery partner will come collect it.</p>
            
            <h3>How Pickup Works:</h3>
            <ol>
                <li>Click "Request Pickup"</li>
                <li>Confirm your location</li>
                <li>Wait for delivery partner</li>
                <li>Hand over the product</li>
                <li>Payment will be processed automatically</li>
            </ol>
        """
        
        return {
            "subject": subject,
            "html": EmailTemplates.get_base_template(
                title=subject,
                content=content,
                action_url=f"https://quicktym.com/rentals/{rental_id}/pickup",
                action_text="Request Pickup"
            ),
            "text": f"Your rental has been active for {duration_hours:.1f} hours. Current cost: ₹{current_cost:.2f}. Request pickup when ready."
        }
    
    @staticmethod
    def rental_completed(
        user_name: str,
        rental_id: str,
        product_name: str,
        total_duration: str,
        total_amount: float,
        payment_status: str
    ) -> Dict[str, str]:
        """Rental completion email."""
        subject = f"Rental Completed - Thank You! 🙏"
        content = f"""
            <h2>Rental Completed Successfully!</h2>
            <p>Hi {user_name},</p>
            <p>Thank you for using QuickTym! Your rental has been completed.</p>
            
            <div class="highlight success">
                <strong>Product:</strong> {product_name}<br>
                <strong>Total Duration:</strong> {total_duration}<br>
                <strong>Total Amount:</strong> ₹{total_amount}<br>
                <strong>Payment Status:</strong> {payment_status.upper()}<br>
            </div>
            
            <h3>How was your experience?</h3>
            <p>Your feedback helps us improve! Please take a moment to review the product and our service.</p>
        """
        
        return {
            "subject": subject,
            "html": EmailTemplates.get_base_template(
                title=subject,
                content=content,
                action_url=f"https://quicktym.com/rentals/{rental_id}/review",
                action_text="Leave a Review"
            ),
            "text": f"Rental completed! Product: {product_name}, Duration: {total_duration}, Amount: ₹{total_amount}"
        }
    
    @staticmethod
    def delivery_partner_assignment(
        partner_name: str,
        delivery_id: str,
        product_name: str,
        customer_name: str,
        pickup_address: str,
        delivery_address: str,
        contact_phone: str
    ) -> Dict[str, str]:
        """New delivery assignment for delivery partner."""
        subject = f"New Delivery Assignment: {delivery_id} 📦"
        content = f"""
            <h2>New Delivery Assignment!</h2>
            <p>Hi {partner_name},</p>
            <p>You have a new delivery assignment.</p>
            
            <div class="highlight">
                <strong>Delivery ID:</strong> {delivery_id}<br>
                <strong>Product:</strong> {product_name}<br>
            </div>
            
            <h3>Pickup Details:</h3>
            <div class="highlight info">
                <strong>Address:</strong> {pickup_address}<br>
                <strong>Contact:</strong> {contact_phone}
            </div>
            
            <h3>Delivery Details:</h3>
            <div class="highlight success">
                <strong>Customer:</strong> {customer_name}<br>
                <strong>Address:</strong> {delivery_address}<br>
            </div>
            
            <p>Please confirm acceptance within 10 minutes.</p>
        """
        
        return {
            "subject": subject,
            "html": EmailTemplates.get_base_template(
                title=subject,
                content=content,
                action_url=f"https://quicktym.com/delivery/{delivery_id}",
                action_text="Accept Assignment"
            ),
            "text": f"New delivery assignment. ID: {delivery_id}, Pickup: {pickup_address}, Delivery: {delivery_address}"
        }
    
    @staticmethod
    def review_request(
        user_name: str,
        rental_id: str,
        product_name: str
    ) -> Dict[str, str]:
        """Request for product review."""
        subject = f"How was {product_name}? ⭐"
        content = f"""
            <h2>Share Your Experience!</h2>
            <p>Hi {user_name},</p>
            <p>We'd love to hear about your experience with <strong>{product_name}</strong>.</p>
            
            <p>Your review helps other users make informed decisions and helps us improve our service.</p>
            
            <div class="highlight">
                <p><strong>What to include in your review:</strong></p>
                <ul>
                    <li>Product quality and condition</li>
                    <li>Delivery experience</li>
                    <li>Value for money</li>
                    <li>Overall satisfaction</li>
                </ul>
            </div>
        """
        
        return {
            "subject": subject,
            "html": EmailTemplates.get_base_template(
                title=subject,
                content=content,
                action_url=f"https://quicktym.com/rentals/{rental_id}/review",
                action_text="Write a Review"
            ),
            "text": f"How was your experience with {product_name}? Leave a review!"
        }
