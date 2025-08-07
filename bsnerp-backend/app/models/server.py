from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class ServerStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"
    ERROR = "error"

class ServerType(str, Enum):
    WEB = "web"
    DATABASE = "database"
    EMAIL = "email"
    DNS = "dns"
    CDN = "cdn"
    BACKUP = "backup"
    OTHER = "other"

class BackupStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"
    SCHEDULED = "scheduled"

class MaintenanceStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Server(BaseModel):
    id: Optional[int] = None
    name: str
    hostname: str
    ip_address: str
    type: ServerType
    status: ServerStatus = ServerStatus.ONLINE
    provider: str
    location: str
    specifications: Dict[str, Any] = {}
    monthly_cost: Optional[float] = None
    ssh_port: int = 22
    ssh_username: str
    ssh_key_path: Optional[str] = None
    monitoring_enabled: bool = True
    backup_enabled: bool = True
    backup_schedule: Optional[str] = None
    last_backup: Optional[datetime] = None
    uptime_percentage: float = 100.0
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    disk_usage: float = 0.0
    network_in: float = 0.0
    network_out: float = 0.0
    installed_software: List[str] = []
    security_updates: List[str] = []
    ssl_certificates: List[Dict[str, Any]] = []
    projects: List[int] = []
    notes: Optional[str] = None
    tags: List[str] = []
    created_at: datetime
    updated_at: datetime

class ServerCreate(BaseModel):
    name: str
    hostname: str
    ip_address: str
    type: ServerType
    provider: str
    location: str
    specifications: Dict[str, Any] = {}
    monthly_cost: Optional[float] = None
    ssh_port: int = 22
    ssh_username: str
    ssh_key_path: Optional[str] = None
    monitoring_enabled: bool = True
    backup_enabled: bool = True
    backup_schedule: Optional[str] = None
    notes: Optional[str] = None
    tags: List[str] = []

class ServerUpdate(BaseModel):
    name: Optional[str] = None
    hostname: Optional[str] = None
    ip_address: Optional[str] = None
    type: Optional[ServerType] = None
    status: Optional[ServerStatus] = None
    provider: Optional[str] = None
    location: Optional[str] = None
    specifications: Optional[Dict[str, Any]] = None
    monthly_cost: Optional[float] = None
    ssh_port: Optional[int] = None
    ssh_username: Optional[str] = None
    ssh_key_path: Optional[str] = None
    monitoring_enabled: Optional[bool] = None
    backup_enabled: Optional[bool] = None
    backup_schedule: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None

class BackupRecord(BaseModel):
    id: Optional[int] = None
    server_id: int
    backup_type: str
    status: BackupStatus
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None

class MaintenanceRecord(BaseModel):
    id: Optional[int] = None
    server_id: int
    title: str
    description: Optional[str] = None
    status: MaintenanceStatus
    scheduled_start: datetime
    scheduled_end: datetime
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    performed_by: Optional[int] = None
    notes: Optional[str] = None
