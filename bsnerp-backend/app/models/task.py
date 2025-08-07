from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    DONE = "done"
    CANCELLED = "cancelled"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class TaskType(str, Enum):
    DEVELOPMENT = "development"
    DESIGN = "design"
    TESTING = "testing"
    REVIEW = "review"
    DOCUMENTATION = "documentation"
    BUG_FIX = "bug_fix"
    FEATURE = "feature"
    MAINTENANCE = "maintenance"

class TimeEntry(BaseModel):
    id: Optional[int] = None
    user_id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    duration: Optional[float] = None
    description: Optional[str] = None
    billable: bool = True

class TaskComment(BaseModel):
    id: Optional[int] = None
    user_id: int
    content: str
    attachments: List[str] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

class SubTask(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    assigned_to: Optional[int] = None
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    project_id: Optional[int] = None
    assigned_to: Optional[int] = None
    created_by: int
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    type: TaskType
    estimated_hours: Optional[float] = None
    actual_hours: float = 0.0
    due_date: Optional[datetime] = None
    start_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    tags: List[str] = []
    attachments: List[str] = []
    subtasks: List[SubTask] = []
    comments: List[TaskComment] = []
    time_entries: List[TimeEntry] = []
    dependencies: List[int] = []
    watchers: List[int] = []
    custom_fields: Dict[str, Any] = {}
    kanban_position: int = 0
    recurring: bool = False
    recurring_pattern: Optional[str] = None
    parent_task_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    project_id: Optional[int] = None
    assigned_to: Optional[int] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    type: TaskType
    estimated_hours: Optional[float] = None
    due_date: Optional[datetime] = None
    start_date: Optional[datetime] = None
    tags: List[str] = []
    subtasks: List[SubTask] = []
    dependencies: List[int] = []
    watchers: List[int] = []
    custom_fields: Dict[str, Any] = {}
    recurring: bool = False
    recurring_pattern: Optional[str] = None
    parent_task_id: Optional[int] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assigned_to: Optional[int] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    type: Optional[TaskType] = None
    estimated_hours: Optional[float] = None
    due_date: Optional[datetime] = None
    start_date: Optional[datetime] = None
    tags: Optional[List[str]] = None
    subtasks: Optional[List[SubTask]] = None
    dependencies: Optional[List[int]] = None
    watchers: Optional[List[int]] = None
    custom_fields: Optional[Dict[str, Any]] = None
    kanban_position: Optional[int] = None

class KanbanMove(BaseModel):
    task_id: int
    new_status: TaskStatus
    new_position: int
