from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class CredentialType(str, Enum):
    DOMAIN = "domain"
    HOSTING = "hosting"
    EMAIL = "email"
    WORDPRESS = "wordpress"
    DATABASE = "database"
    FTP = "ftp"
    SSH = "ssh"
    API = "api"
    SOCIAL_MEDIA = "social_media"
    OTHER = "other"

class CredentialStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    EXPIRING_SOON = "expiring_soon"
    INACTIVE = "inactive"

class Credential(BaseModel):
    id: Optional[int] = None
    name: str
    type: CredentialType
    status: CredentialStatus = CredentialStatus.ACTIVE
    client_id: Optional[int] = None
    project_id: Optional[int] = None
    server_id: Optional[int] = None
    url: Optional[str] = None
    username: str
    password: str
    email: Optional[str] = None
    additional_info: Dict[str, Any] = {}
    expiry_date: Optional[datetime] = None
    renewal_date: Optional[datetime] = None
    auto_renewal: bool = False
    cost: Optional[float] = None
    provider: Optional[str] = None
    notes: Optional[str] = None
    tags: List[str] = []
    shared_with: List[int] = []
    last_tested: Optional[datetime] = None
    test_status: Optional[str] = None
    backup_codes: List[str] = []
    two_factor_enabled: bool = False
    created_at: datetime
    updated_at: datetime

class CredentialCreate(BaseModel):
    name: str
    type: CredentialType
    client_id: Optional[int] = None
    project_id: Optional[int] = None
    server_id: Optional[int] = None
    url: Optional[str] = None
    username: str
    password: str
    email: Optional[str] = None
    additional_info: Dict[str, Any] = {}
    expiry_date: Optional[datetime] = None
    renewal_date: Optional[datetime] = None
    auto_renewal: bool = False
    cost: Optional[float] = None
    provider: Optional[str] = None
    notes: Optional[str] = None
    tags: List[str] = []
    shared_with: List[int] = []
    backup_codes: List[str] = []
    two_factor_enabled: bool = False

class CredentialUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[CredentialType] = None
    status: Optional[CredentialStatus] = None
    client_id: Optional[int] = None
    project_id: Optional[int] = None
    server_id: Optional[int] = None
    url: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    additional_info: Optional[Dict[str, Any]] = None
    expiry_date: Optional[datetime] = None
    renewal_date: Optional[datetime] = None
    auto_renewal: Optional[bool] = None
    cost: Optional[float] = None
    provider: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    shared_with: Optional[List[int]] = None
    backup_codes: Optional[List[str]] = None
    two_factor_enabled: Optional[bool] = None

class PasswordStrength(BaseModel):
    score: int
    feedback: List[str]
    suggestions: List[str]

class ConnectionTest(BaseModel):
    credential_id: int
    success: bool
    response_time: Optional[float] = None
    error_message: Optional[str] = None
    tested_at: datetime
