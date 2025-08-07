from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class ClientStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PROSPECT = "prospect"
    SUSPENDED = "suspended"

class ClientType(str, Enum):
    INDIVIDUAL = "individual"
    COMPANY = "company"
    AGENCY = "agency"

class ContactPerson(BaseModel):
    name: str
    email: EmailStr
    phone: str
    position: str
    is_primary: bool = False

class Client(BaseModel):
    id: Optional[int] = None
    name: str
    email: EmailStr
    phone: str
    type: ClientType
    status: ClientStatus = ClientStatus.ACTIVE
    company_name: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    tax_number: Optional[str] = None
    contact_persons: List[ContactPerson] = []
    notes: Optional[str] = None
    tags: List[str] = []
    source: Optional[str] = None
    assigned_manager: Optional[int] = None
    total_projects: int = 0
    total_revenue: float = 0.0
    last_project_date: Optional[datetime] = None
    documents: List[str] = []
    custom_fields: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime

class ClientCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    type: ClientType
    company_name: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    tax_number: Optional[str] = None
    contact_persons: List[ContactPerson] = []
    notes: Optional[str] = None
    tags: List[str] = []
    source: Optional[str] = None
    assigned_manager: Optional[int] = None
    custom_fields: Dict[str, Any] = {}

class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    type: Optional[ClientType] = None
    status: Optional[ClientStatus] = None
    company_name: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    tax_number: Optional[str] = None
    contact_persons: Optional[List[ContactPerson]] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    source: Optional[str] = None
    assigned_manager: Optional[int] = None
    custom_fields: Optional[Dict[str, Any]] = None

class ClientFilter(BaseModel):
    status: Optional[ClientStatus] = None
    type: Optional[ClientType] = None
    assigned_manager: Optional[int] = None
    city: Optional[str] = None
    country: Optional[str] = None
    tags: Optional[List[str]] = None
    search: Optional[str] = None
    created_from: Optional[datetime] = None
    created_to: Optional[datetime] = None
