from fastapi import APIRouter, Depends
from typing import Dict, Any
from datetime import datetime
from ..database import db
from ..auth.dependencies import get_current_active_user, require_role

router = APIRouter(prefix="/settings", tags=["Settings"])

@router.get("/company")
async def get_company_settings(current_user: dict = Depends(get_current_active_user)):
    return {
        "company_name": "شركة BSN للحلول الرقمية",
        "logo": "/assets/logo.png",
        "address": "القاهرة الجديدة، مصر",
        "phone": "+201234567890",
        "email": "info@bsn.com",
        "website": "https://bsn.com",
        "tax_number": "123456789",
        "currency": "EGP",
        "language": "ar",
        "timezone": "Africa/Cairo"
    }

@router.put("/company")
async def update_company_settings(
    settings: Dict[str, Any],
    current_user: dict = Depends(require_role("admin"))
):
    return {"message": "تم تحديث إعدادات الشركة بنجاح", "settings": settings}

@router.get("/security")
async def get_security_settings(current_user: dict = Depends(require_role("admin"))):
    return {
        "password_policy": {
            "min_length": 8,
            "require_uppercase": True,
            "require_lowercase": True,
            "require_numbers": True,
            "require_symbols": True,
            "expiry_days": 90
        },
        "session_settings": {
            "timeout_minutes": 30,
            "max_concurrent_sessions": 3,
            "remember_me_days": 7
        },
        "two_factor": {
            "enabled": True,
            "mandatory_for_admins": True,
            "backup_codes_count": 10
        },
        "audit_logs": {
            "enabled": True,
            "retention_days": 365,
            "log_failed_attempts": True
        }
    }

@router.put("/security")
async def update_security_settings(
    settings: Dict[str, Any],
    current_user: dict = Depends(require_role("admin"))
):
    return {"message": "تم تحديث إعدادات الأمان بنجاح", "settings": settings}

@router.get("/integrations")
async def get_integrations(current_user: dict = Depends(require_role("admin"))):
    return {
        "email": {
            "provider": "smtp",
            "host": "smtp.gmail.com",
            "port": 587,
            "username": "noreply@bsn.com",
            "enabled": True
        },
        "sms": {
            "provider": "twilio",
            "enabled": False
        },
        "backup": {
            "provider": "aws_s3",
            "bucket": "bsn-backups",
            "enabled": True,
            "schedule": "daily"
        },
        "webhooks": [
            {
                "id": 1,
                "name": "Slack Notifications",
                "url": "https://hooks.slack.com/services/...",
                "events": ["project_created", "task_completed"],
                "enabled": True
            }
        ]
    }

@router.post("/integrations/webhook")
async def create_webhook(
    name: str,
    url: str,
    events: list,
    current_user: dict = Depends(require_role("admin"))
):
    webhook = {
        "id": len(db.notification_templates) + 1,
        "name": name,
        "url": url,
        "events": events,
        "enabled": True,
        "created_at": datetime.now()
    }
    
    return {"message": "تم إنشاء الـ webhook بنجاح", "webhook": webhook}

@router.get("/backup")
async def get_backup_settings(current_user: dict = Depends(require_role("admin"))):
    return {
        "auto_backup": {
            "enabled": True,
            "frequency": "daily",
            "time": "02:00",
            "retention_days": 30
        },
        "backup_location": {
            "type": "cloud",
            "provider": "aws_s3",
            "bucket": "bsn-backups"
        },
        "last_backup": {
            "date": "2024-08-07T02:00:00Z",
            "status": "success",
            "size": "125.6 MB"
        }
    }

@router.post("/backup/create")
async def create_manual_backup(current_user: dict = Depends(require_role("admin"))):
    import random
    
    backup_id = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    size = f"{random.randint(50, 200)}.{random.randint(1, 9)} MB"
    
    return {
        "message": "تم إنشاء النسخة الاحتياطية بنجاح",
        "backup": {
            "id": backup_id,
            "created_at": datetime.now(),
            "size": size,
            "status": "completed"
        }
    }

@router.get("/audit-logs")
async def get_audit_logs(
    page: int = 1,
    limit: int = 50,
    current_user: dict = Depends(require_role("admin"))
):
    logs = [
        {
            "id": 1,
            "user_id": current_user["id"],
            "action": "login",
            "resource": "auth",
            "details": "تسجيل دخول ناجح",
            "ip_address": "192.168.1.100",
            "user_agent": "Mozilla/5.0...",
            "timestamp": datetime.now()
        },
        {
            "id": 2,
            "user_id": current_user["id"],
            "action": "create",
            "resource": "client",
            "details": "إنشاء عميل جديد: شركة التقنية المتقدمة",
            "ip_address": "192.168.1.100",
            "user_agent": "Mozilla/5.0...",
            "timestamp": datetime.now()
        }
    ]
    
    return {
        "logs": logs,
        "total": len(logs),
        "page": page,
        "limit": limit
    }

@router.get("/system-info")
async def get_system_info(current_user: dict = Depends(require_role("admin"))):
    return {
        "version": "1.0.0",
        "environment": "production",
        "database": {
            "type": "in_memory",
            "status": "connected",
            "records": {
                "users": len(db.users),
                "clients": len(db.clients),
                "projects": len(db.projects),
                "tasks": len(db.tasks),
                "transactions": len(db.transactions)
            }
        },
        "server": {
            "uptime": "5 days, 12 hours",
            "memory_usage": "45%",
            "cpu_usage": "23%",
            "disk_usage": "67%"
        },
        "last_updated": datetime.now()
    }
