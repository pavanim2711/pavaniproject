"""WebSocket connection manager for real-time notifications."""

from typing import Dict, List, Set, Optional, Any
from datetime import datetime
import json
import asyncio
import logging
from fastapi import WebSocket

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manage WebSocket connections for real-time updates."""
    
    def __init__(self):
        # user_id -> set of websocket connections
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        # connection -> user_id mapping
        self.connection_user_map: Dict[WebSocket, str] = {}
        # user_id -> list of undelivered messages
        self.message_queue: Dict[str, List[Dict[str, Any]]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str):
        """
        Accept a new WebSocket connection and associate it with a user.
        
        Args:
            websocket: WebSocket connection
            user_id: User ID associated with this connection
        """
        await websocket.accept()
        
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        
        self.active_connections[user_id].add(websocket)
        self.connection_user_map[websocket] = user_id
        
        logger.info(f"WebSocket connected for user {user_id}")
        
        # Send any queued messages
        if user_id in self.message_queue and self.message_queue[user_id]:
            for message in self.message_queue[user_id]:
                try:
                    await websocket.send_json(message)
                except Exception as e:
                    logger.error(f"Error sending queued message: {e}")
            
            # Clear queue after sending
            self.message_queue[user_id] = []
    
    def disconnect(self, websocket: WebSocket):
        """
        Remove a WebSocket connection.
        
        Args:
            websocket: WebSocket connection to remove
        """
        user_id = self.connection_user_map.get(websocket)
        
        if user_id:
            if user_id in self.active_connections:
                self.active_connections[user_id].discard(websocket)
                
                # Clean up empty sets
                if not self.active_connections[user_id]:
                    del self.active_connections[user_id]
            
            del self.connection_user_map[websocket]
            logger.info(f"WebSocket disconnected for user {user_id}")
    
    async def send_personal_message(
        self,
        user_id: str,
        message: Dict[str, Any],
        queue_if_offline: bool = True
    ):
        """
        Send a message to all connections of a specific user.
        
        Args:
            user_id: Target user ID
            message: Message dictionary to send
            queue_if_offline: If True, queue message when user is offline
        """
        if user_id in self.active_connections and self.active_connections[user_id]:
            # Add timestamp if not present
            if "timestamp" not in message:
                message["timestamp"] = datetime.utcnow().isoformat()
            
            # Send to all user's connections
            disconnected = []
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error sending message to user {user_id}: {e}")
                    disconnected.append(connection)
            
            # Clean up disconnected connections
            for conn in disconnected:
                self.disconnect(conn)
        elif queue_if_offline:
            # Queue message for offline user
            if user_id not in self.message_queue:
                self.message_queue[user_id] = []
            
            if "timestamp" not in message:
                message["timestamp"] = datetime.utcnow().isoformat()
            
            self.message_queue[user_id].append(message)
            logger.info(f"Message queued for offline user {user_id}")
    
    async def broadcast(
        self,
        message: Dict[str, Any],
        exclude_user: Optional[str] = None
    ):
        """
        Broadcast a message to all connected users.
        
        Args:
            message: Message dictionary to broadcast
            exclude_user: Optional user ID to exclude from broadcast
        """
        if "timestamp" not in message:
            message["timestamp"] = datetime.utcnow().isoformat()
        
        for user_id in list(self.active_connections.keys()):
            if exclude_user and user_id == exclude_user:
                continue
            
            await self.send_personal_message(user_id, message, queue_if_offline=False)
    
    async def broadcast_to_role(
        self,
        role: str,
        message: Dict[str, Any],
        db=None
    ):
        """
        Broadcast a message to all users with a specific role.
        
        Args:
            role: User role (Customer, Delivery_Partner, Admin)
            message: Message dictionary to broadcast
            db: Database session to fetch users by role
        """
        # This would need to be implemented with database query
        # For now, we'll use the connection map
        # In production, you'd query the database for users with the role
        pass
    
    def get_online_users(self) -> List[str]:
        """Get list of currently online user IDs."""
        return list(self.active_connections.keys())
    
    def is_user_online(self, user_id: str) -> bool:
        """Check if a user is currently online."""
        return user_id in self.active_connections and len(self.active_connections[user_id]) > 0
    
    def get_connection_count(self, user_id: str) -> int:
        """Get number of active connections for a user."""
        if user_id in self.active_connections:
            return len(self.active_connections[user_id])
        return 0


# Singleton instance
connection_manager = ConnectionManager()


# ==================== Notification Types ====================

class NotificationType:
    """Notification type constants."""
    
    # Rental notifications
    RENTAL_CREATED = "rental_created"
    RENTAL_STARTED = "rental_started"
    RENTAL_COMPLETED = "rental_completed"
    RENTAL_CANCELLED = "rental_cancelled"
    PICKUP_REMINDER = "pickup_reminder"
    
    # Delivery notifications
    DELIVERY_ASSIGNED = "delivery_assigned"
    DELIVERY_STATUS_UPDATE = "delivery_status_update"
    DELIVERY_PARTNER_ASSIGNED = "delivery_partner_assigned"
    DELIVERY_LOCATION_UPDATE = "delivery_location_update"
    
    # Payment notifications
    PAYMENT_SUCCESS = "payment_success"
    PAYMENT_FAILED = "payment_failed"
    REFUND_PROCESSED = "refund_processed"
    
    # Review notifications
    REVIEW_REQUEST = "review_request"
    REVIEW_RECEIVED = "review_received"
    
    # Admin notifications
    ADMIN_ALERT = "admin_alert"
    NEW_ORDER = "new_order"
    
    # System notifications
    SYSTEM_ANNOUNCEMENT = "system_announcement"
    MAINTENANCE_ALERT = "maintenance_alert"


# ==================== Notification Helper ====================

class NotificationHelper:
    """Helper class for creating notifications."""
    
    @staticmethod
    async def notify_rental_update(
        user_id: str,
        rental_id: str,
        status: str,
        message: str,
        additional_data: Optional[Dict[str, Any]] = None
    ):
        """
        Send rental update notification.
        
        Args:
            user_id: User ID to notify
            rental_id: Rental session ID
            status: New rental status
            message: Notification message
            additional_data: Additional data to include
        """
        notification = {
            "type": NotificationType.RENTAL_STARTED if status == "active" else f"rental_{status}",
            "rental_id": rental_id,
            "status": status,
            "message": message,
            "data": additional_data
        }
        
        await connection_manager.send_personal_message(user_id, notification)
    
    @staticmethod
    async def notify_delivery_update(
        user_id: str,
        delivery_id: str,
        status: str,
        partner_name: Optional[str] = None,
        estimated_time: Optional[str] = None
    ):
        """
        Send delivery status update notification.
        
        Args:
            user_id: User ID to notify
            delivery_id: Delivery ID
            status: Delivery status
            partner_name: Delivery partner name
            estimated_time: Estimated delivery time
        """
        notification = {
            "type": NotificationType.DELIVERY_STATUS_UPDATE,
            "delivery_id": delivery_id,
            "status": status,
            "partner_name": partner_name,
            "estimated_time": estimated_time,
            "message": f"Delivery status updated to: {status}"
        }
        
        await connection_manager.send_personal_message(user_id, notification)
    
    @staticmethod
    async def notify_delivery_partner(
        partner_id: str,
        delivery_id: str,
        pickup_address: str,
        delivery_address: str,
        product_name: str
    ):
        """
        Send new delivery assignment notification to partner.
        
        Args:
            partner_id: Delivery partner user ID
            delivery_id: Delivery ID
            pickup_address: Pickup location
            delivery_address: Delivery location
            product_name: Product name
        """
        notification = {
            "type": NotificationType.DELIVERY_PARTNER_ASSIGNED,
            "delivery_id": delivery_id,
            "pickup_address": pickup_address,
            "delivery_address": delivery_address,
            "product_name": product_name,
            "message": "New delivery assignment received",
            "action_required": True
        }
        
        await connection_manager.send_personal_message(partner_id, notification)
    
    @staticmethod
    async def notify_payment_status(
        user_id: str,
        payment_id: str,
        amount: float,
        status: str,
        rental_id: str
    ):
        """
        Send payment status notification.
        
        Args:
            user_id: User ID to notify
            payment_id: Payment ID
            amount: Payment amount
            status: Payment status
            rental_id: Rental session ID
        """
        notification = {
            "type": NotificationType.PAYMENT_SUCCESS if status == "completed" else NotificationType.PAYMENT_FAILED,
            "payment_id": payment_id,
            "rental_id": rental_id,
            "amount": amount,
            "status": status,
            "message": f"Payment of ₹{amount} {status}"
        }
        
        await connection_manager.send_personal_message(user_id, notification)
    
    @staticmethod
    async def broadcast_system_announcement(
        title: str,
        message: str,
        priority: str = "normal"
    ):
        """
        Broadcast system-wide announcement.
        
        Args:
            title: Announcement title
            message: Announcement message
            priority: Priority level (low, normal, high)
        """
        notification = {
            "type": NotificationType.SYSTEM_ANNOUNCEMENT,
            "title": title,
            "message": message,
            "priority": priority
        }
        
        await connection_manager.broadcast(notification)


# Singleton instance
notification_helper = NotificationHelper()
