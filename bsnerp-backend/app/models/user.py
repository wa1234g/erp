from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"
    CLIENT = "client"

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

class User(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    username: str
    full_name: str
    phone: Optional[str] = None
    role: UserRole
    status: UserStatus = UserStatus.ACTIVE
    avatar: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    skills: List[str] = []
    permissions: List[str] = []
    two_factor_enabled: bool = False
    two_factor_secret: Optional[str] = None
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    password_hash: str
    reset_token: Optional[str] = None
    reset_token_expires: Optional[datetime] = None
    email_verified: bool = False
    verification_token: Optional[str] = None

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    phone: Optional[str] = None
    role: UserRole
    department: Optional[str] = None
    position: Optional[str] = None
    skills: List[str] = []
    permissions: List[str] = []
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None
    department: Optional[str] = None
    position: Optional[str] = None
    skills: Optional[List[str]] = None
    permissions: Optional[List[str]] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = False
    two_factor_code: Optional[str] = None

class PasswordReset(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str

class TwoFactorSetup(BaseModel):
    secret: str
    code: str
