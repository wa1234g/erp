from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class NotificationType(str, Enum):
    RENEWAL_REMINDER = "renewal_reminder"
    PROJECT_UPDATE = "project_update"
    TASK_ASSIGNMENT = "task_assignment"
    PAYMENT_DUE = "payment_due"
    SERVER_ALERT = "server_alert"
    BACKUP_STATUS = "backup_status"
    SECURITY_ALERT = "security_alert"
    CUSTOM = "custom"

class NotificationChannel(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    IN_APP = "in_app"
    WEBHOOK = "webhook"
    SLACK = "slack"
    TELEGRAM = "telegram"

class NotificationStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    READ = "read"

class NotificationPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class Notification(BaseModel):
    id: Optional[int] = None
    type: NotificationType
    title: str
    message: str
    priority: NotificationPriority = NotificationPriority.MEDIUM
    channels: List[NotificationChannel]
    recipients: List[int]
    status: NotificationStatus = NotificationStatus.PENDING
    scheduled_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    template_id: Optional[int] = None
    data: Dict[str, Any] = {}
    retry_count: int = 0
    max_retries: int = 3
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class NotificationTemplate(BaseModel):
    id: Optional[int] = None
    name: str
    type: NotificationType
    title_template: str
    message_template: str
    default_channels: List[NotificationChannel]
    variables: List[str] = []
    active: bool = True
    created_at: datetime
    updated_at: datetime

class NotificationSubscription(BaseModel):
    id: Optional[int] = None
    user_id: int
    notification_type: NotificationType
    channels: List[NotificationChannel]
    enabled: bool = True
    filters: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime

class NotificationCreate(BaseModel):
    type: NotificationType
    title: str
    message: str
    priority: NotificationPriority = NotificationPriority.MEDIUM
    channels: List[NotificationChannel]
    recipients: List[int]
    scheduled_at: Optional[datetime] = None
    template_id: Optional[int] = None
    data: Dict[str, Any] = {}

class NotificationUpdate(BaseModel):
    title: Optional[str] = None
    message: Optional[str] = None
    priority: Optional[NotificationPriority] = None
    channels: Optional[List[NotificationChannel]] = None
    recipients: Optional[List[int]] = None
    scheduled_at: Optional[datetime] = None
    status: Optional[NotificationStatus] = None
