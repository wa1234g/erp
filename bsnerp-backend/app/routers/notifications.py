from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from datetime import datetime, timedelta
from ..models.notification import Notification, NotificationCreate, NotificationUpdate, NotificationTemplate, NotificationSubscription
from ..database import db
from ..auth.dependencies import get_current_active_user

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/", response_model=dict)
async def get_notifications(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    type: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    current_user: dict = Depends(get_current_active_user)
):
    notifications = list(db.notifications.values())
    
    user_notifications = [n for n in notifications if current_user["id"] in n.get("recipients", [])]
    
    if type:
        user_notifications = [n for n in user_notifications if n["type"] == type]
    
    if status:
        user_notifications = [n for n in user_notifications if n["status"] == status]
    
    if priority:
        user_notifications = [n for n in user_notifications if n["priority"] == priority]
    
    user_notifications.sort(key=lambda x: x["created_at"], reverse=True)
    
    total = len(user_notifications)
    start = (page - 1) * limit
    end = start + limit
    user_notifications = user_notifications[start:end]
    
    return {
        "notifications": user_notifications,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    }

@router.post("/", response_model=Notification)
async def create_notification(
    notification_data: NotificationCreate,
    current_user: dict = Depends(get_current_active_user)
):
    notification_id = db._get_next_id('notifications')
    now = datetime.now()
    
    notification = {
        "id": notification_id,
        **notification_data.dict(),
        "status": "pending",
        "sent_at": None,
        "delivered_at": None,
        "read_at": None,
        "retry_count": 0,
        "max_retries": 3,
        "error_message": None,
        "created_at": now,
        "updated_at": now
    }
    
    db.notifications[notification_id] = notification
    
    if not notification_data.scheduled_at or notification_data.scheduled_at <= now:
        notification["status"] = "sent"
        notification["sent_at"] = now
        notification["delivered_at"] = now
        db.notifications[notification_id] = notification
    
    return notification

@router.put("/{notification_id}", response_model=Notification)
async def update_notification(
    notification_id: int,
    notification_data: NotificationUpdate,
    current_user: dict = Depends(get_current_active_user)
):
    notification = db.notifications.get(notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="الإشعار غير موجود")
    
    update_data = notification_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        notification[key] = value
    
    notification["updated_at"] = datetime.now()
    db.notifications[notification_id] = notification
    return notification

@router.post("/{notification_id}/mark-read")
async def mark_notification_read(
    notification_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    notification = db.notifications.get(notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="الإشعار غير موجود")
    
    if current_user["id"] not in notification.get("recipients", []):
        raise HTTPException(status_code=403, detail="غير مصرح لك بقراءة هذا الإشعار")
    
    notification["status"] = "read"
    notification["read_at"] = datetime.now()
    notification["updated_at"] = datetime.now()
    db.notifications[notification_id] = notification
    
    return {"message": "تم تحديد الإشعار كمقروء"}

@router.post("/mark-all-read")
async def mark_all_notifications_read(current_user: dict = Depends(get_current_active_user)):
    updated_count = 0
    now = datetime.now()
    
    for notification in db.notifications.values():
        if (current_user["id"] in notification.get("recipients", []) and 
            notification["status"] != "read"):
            notification["status"] = "read"
            notification["read_at"] = now
            notification["updated_at"] = now
            updated_count += 1
    
    return {"message": f"تم تحديد {updated_count} إشعار كمقروء"}

@router.get("/templates", response_model=List[NotificationTemplate])
async def get_notification_templates(current_user: dict = Depends(get_current_active_user)):
    return list(db.notification_templates.values())

@router.post("/templates", response_model=NotificationTemplate)
async def create_notification_template(
    name: str,
    type: str,
    title_template: str,
    message_template: str,
    default_channels: List[str],
    current_user: dict = Depends(get_current_active_user)
):
    template_id = db._get_next_id('notification_templates')
    now = datetime.now()
    
    template = {
        "id": template_id,
        "name": name,
        "type": type,
        "title_template": title_template,
        "message_template": message_template,
        "default_channels": default_channels,
        "variables": [],
        "active": True,
        "created_at": now,
        "updated_at": now
    }
    
    db.notification_templates[template_id] = template
    return template

@router.get("/subscriptions")
async def get_user_subscriptions(current_user: dict = Depends(get_current_active_user)):
    subscriptions = [s for s in db.notification_subscriptions.values() 
                    if s["user_id"] == current_user["id"]]
    return {"subscriptions": subscriptions}

@router.post("/subscriptions")
async def create_subscription(
    notification_type: str,
    channels: List[str],
    enabled: bool = True,
    current_user: dict = Depends(get_current_active_user)
):
    subscription_id = db._get_next_id('notification_subscriptions')
    now = datetime.now()
    
    subscription = {
        "id": subscription_id,
        "user_id": current_user["id"],
        "notification_type": notification_type,
        "channels": channels,
        "enabled": enabled,
        "filters": {},
        "created_at": now,
        "updated_at": now
    }
    
    db.notification_subscriptions[subscription_id] = subscription
    return subscription

@router.post("/send-renewal-reminders")
async def send_renewal_reminders(current_user: dict = Depends(get_current_active_user)):
    now = datetime.now()
    reminder_threshold = now + timedelta(days=30)
    
    expiring_credentials = []
    for credential in db.credentials.values():
        if credential.get("expiry_date"):
            expiry_date = credential["expiry_date"]
            if isinstance(expiry_date, str):
                expiry_date = datetime.fromisoformat(expiry_date.replace('Z', '+00:00'))
            
            if expiry_date <= reminder_threshold:
                expiring_credentials.append(credential)
    
    notifications_sent = 0
    for credential in expiring_credentials:
        notification_id = db._get_next_id('notifications')
        
        days_until_expiry = (credential["expiry_date"] - now).days if credential.get("expiry_date") else 0
        
        notification = {
            "id": notification_id,
            "type": "renewal_reminder",
            "title": f"تذكير تجديد: {credential['name']}",
            "message": f"ستنتهي صلاحية {credential['name']} خلال {days_until_expiry} يوم",
            "priority": "high" if days_until_expiry <= 7 else "medium",
            "channels": ["email", "in_app"],
            "recipients": [current_user["id"]],
            "status": "sent",
            "scheduled_at": None,
            "sent_at": now,
            "delivered_at": now,
            "read_at": None,
            "template_id": None,
            "data": {"credential_id": credential["id"], "days_until_expiry": days_until_expiry},
            "retry_count": 0,
            "max_retries": 3,
            "error_message": None,
            "created_at": now,
            "updated_at": now
        }
        
        db.notifications[notification_id] = notification
        notifications_sent += 1
    
    return {"message": f"تم إرسال {notifications_sent} تذكير تجديد"}

@router.get("/stats/overview")
async def get_notifications_stats(current_user: dict = Depends(get_current_active_user)):
    user_notifications = [n for n in db.notifications.values() 
                         if current_user["id"] in n.get("recipients", [])]
    
    total_notifications = len(user_notifications)
    unread_notifications = len([n for n in user_notifications if n["status"] != "read"])
    high_priority = len([n for n in user_notifications if n["priority"] == "high"])
    
    return {
        "total_notifications": total_notifications,
        "unread_notifications": unread_notifications,
        "high_priority_notifications": high_priority,
        "read_rate": ((total_notifications - unread_notifications) / total_notifications * 100) if total_notifications > 0 else 0
    }
