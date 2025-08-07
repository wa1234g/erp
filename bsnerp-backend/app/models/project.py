from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class ProjectStatus(str, Enum):
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ARCHIVED = "archived"

class ProjectType(str, Enum):
    WEBSITE = "website"
    ECOMMERCE = "ecommerce"
    MOBILE_APP = "mobile_app"
    WORDPRESS = "wordpress"
    MAINTENANCE = "maintenance"
    DESIGN = "design"
    MARKETING = "marketing"
    CUSTOM = "custom"

class ProjectPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class ProjectPhase(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: ProjectStatus
    progress: float = 0.0
    budget: Optional[float] = None
    actual_cost: float = 0.0
    deliverables: List[str] = []

class TeamMember(BaseModel):
    user_id: int
    role: str
    hourly_rate: Optional[float] = None
    allocated_hours: Optional[float] = None
    actual_hours: float = 0.0

class Project(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    client_id: int
    type: ProjectType
    status: ProjectStatus = ProjectStatus.PLANNING
    priority: ProjectPriority = ProjectPriority.MEDIUM
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    estimated_hours: Optional[float] = None
    actual_hours: float = 0.0
    budget: Optional[float] = None
    actual_cost: float = 0.0
    progress: float = 0.0
    phases: List[ProjectPhase] = []
    team_members: List[TeamMember] = []
    tags: List[str] = []
    files: List[str] = []
    notes: Optional[str] = None
    requirements: Optional[str] = None
    deliverables: List[str] = []
    milestones: List[Dict[str, Any]] = []
    risks: List[Dict[str, Any]] = []
    custom_fields: Dict[str, Any] = {}
    template_id: Optional[int] = None
    parent_project_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    client_id: int
    type: ProjectType
    priority: ProjectPriority = ProjectPriority.MEDIUM
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    estimated_hours: Optional[float] = None
    budget: Optional[float] = None
    phases: List[ProjectPhase] = []
    team_members: List[TeamMember] = []
    tags: List[str] = []
    notes: Optional[str] = None
    requirements: Optional[str] = None
    deliverables: List[str] = []
    custom_fields: Dict[str, Any] = {}
    template_id: Optional[int] = None

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[ProjectType] = None
    status: Optional[ProjectStatus] = None
    priority: Optional[ProjectPriority] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    estimated_hours: Optional[float] = None
    budget: Optional[float] = None
    progress: Optional[float] = None
    phases: Optional[List[ProjectPhase]] = None
    team_members: Optional[List[TeamMember]] = None
    tags: Optional[List[str]] = None
    notes: Optional[str] = None
    requirements: Optional[str] = None
    deliverables: Optional[List[str]] = None
    custom_fields: Optional[Dict[str, Any]] = None
