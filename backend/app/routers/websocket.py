"""WebSocket router for real-time notifications."""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
import json
import logging

from app.db.session import get_db
from app.models.user import User
from app.core.jwt import verify_access_token
from app.services.websocket_manager import connection_manager, notification_helper

logger = logging.getLogger(__name__)

router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws/notifications")
async def websocket_notifications(
    websocket: WebSocket,
    token: str = Query(..., description="JWT authentication token"),
    db: Session = Depends(get_db)
):
    """
    WebSocket endpoint for real-time notifications.
    
    Connect with: ws://localhost:8000/ws/notifications?token=YOUR_JWT_TOKEN
    
    Message format received:
    {
        "type": "notification_type",
        "data": {...},
        "message": "Human readable message",
        "timestamp": "2024-01-15T10:30:00"
    }
    
    Client can send:
    - ping: Keep connection alive
    - mark_read: Mark notification as read
    """
    # Verify token
    payload = verify_access_token(token)
    if not payload:
        await websocket.close(code=4001, reason="Invalid authentication token")
        return
    
    user_id = payload.get("sub")
    if not user_id:
        await websocket.close(code=4001, reason="Invalid token payload")
        return
    
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        await websocket.close(code=4004, reason="User not found")
        return
    
    # Connect
    await connection_manager.connect(websocket, str(user_id))
    
    try:
        # Send welcome message
        await websocket.send_json({
            "type": "connected",
            "message": f"Welcome {user.name}! You are now connected to real-time notifications.",
            "user_id": str(user_id)
        })
        
        # Listen for messages
        while True:
            try:
                data = await websocket.receive_text()
                
                # Parse message
                try:
                    message = json.loads(data)
                except json.JSONDecodeError:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Invalid JSON format"
                    })
                    continue
                
                # Handle different message types
                message_type = message.get("type")
                
                if message_type == "ping":
                    # Keep-alive ping
                    await websocket.send_json({
                        "type": "pong",
                        "timestamp": datetime.utcnow().isoformat()
                    })
                
                elif message_type == "mark_read":
                    # Mark notification as read
                    notification_id = message.get("notification_id")
                    # TODO: Update notification in database
                    await websocket.send_json({
                        "type": "marked_read",
                        "notification_id": notification_id
                    })
                
                elif message_type == "get_online":
                    # Get list of online users (admin only)
                    if user.role == "Admin":
                        online_users = connection_manager.get_online_users()
                        await websocket.send_json({
                            "type": "online_users",
                            "users": online_users,
                            "count": len(online_users)
                        })
                    else:
                        await websocket.send_json({
                            "type": "error",
                            "message": "Unauthorized: Admin only"
                        })
                
                else:
                    await websocket.send_json({
                        "type": "error",
                        "message": f"Unknown message type: {message_type}"
                    })
            
            except WebSocketDisconnect:
                logger.info(f"WebSocket disconnected for user {user_id}")
                break
            
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                await websocket.send_json({
                    "type": "error",
                    "message": "Internal server error"
                })
    
    except WebSocketDisconnect:
        pass
    
    finally:
        connection_manager.disconnect(websocket)


# ==================== REST Endpoints for Notifications ====================

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Any

# Create a separate router for REST endpoints
notifications_router = APIRouter(prefix="/notifications", tags=["Notifications"])


class NotificationSend(BaseModel):
    """Request model for sending notification."""
    user_id: str
    type: str
    message: str
    data: Optional[Dict[str, Any]] = None


class BroadcastRequest(BaseModel):
    """Request model for broadcast notification."""
    type: str
    title: str
    message: str
    priority: str = "normal"


@notifications_router.get("/status")
async def get_notification_status(
    user_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get notification system status.
    
    Returns online users count and queue status.
    """
    online_users = connection_manager.get_online_users()
    
    return {
        "online_users_count": len(online_users),
        "queued_messages": sum(len(q) for q in connection_manager.message_queue.values()),
        "total_connections": sum(connection_manager.get_connection_count(uid) for uid in online_users)
    }


@notifications_router.post("/send")
async def send_notification(
    notification: NotificationSend,
    db: Session = Depends(get_db)
):
    """
    Send a notification to a specific user.
    
    For testing/admin use.
    """
    await connection_manager.send_personal_message(
        user_id=notification.user_id,
        message={
            "type": notification.type,
            "message": notification.message,
            "data": notification.data
        }
    )
    
    return {
        "success": True,
        "message": f"Notification sent to user {notification.user_id}"
    }


@notifications_router.post("/broadcast")
async def broadcast_notification(
    broadcast: BroadcastRequest,
    db: Session = Depends(get_db)
):
    """
    Broadcast a notification to all connected users.
    
    Admin only.
    """
    # TODO: Add admin authentication check
    
    await notification_helper.broadcast_system_announcement(
        title=broadcast.title,
        message=broadcast.message,
        priority=broadcast.priority
    )
    
    return {
        "success": True,
        "message": "Notification broadcasted to all users"
    }


@notifications_router.get("/online-users")
async def get_online_users(db: Session = Depends(get_db)):
    """
    Get list of currently online users.
    
    Admin only.
    """
    # TODO: Add admin authentication check
    
    online_users = connection_manager.get_online_users()
    
    return {
        "online_users": online_users,
        "count": len(online_users)
    }


@notifications_router.get("/user/{user_id}/status")
async def get_user_connection_status(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    Check if a specific user is online.
    """
    is_online = connection_manager.is_user_online(user_id)
    connection_count = connection_manager.get_connection_count(user_id)
    
    return {
        "user_id": user_id,
        "is_online": is_online,
        "connection_count": connection_count
    }


# Import datetime for pong response
from datetime import datetime
