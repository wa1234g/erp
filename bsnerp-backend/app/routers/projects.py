from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from datetime import datetime
from ..models.project import Project, ProjectCreate, ProjectUpdate
from ..database import db
from ..auth.dependencies import get_current_active_user

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("/", response_model=dict)
async def get_projects(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    status: Optional[str] = None,
    type: Optional[str] = None,
    client_id: Optional[int] = None,
    current_user: dict = Depends(get_current_active_user)
):
    projects = list(db.projects.values())
    
    if search:
        projects = [p for p in projects if search.lower() in p["name"].lower()]
    
    if status:
        projects = [p for p in projects if p["status"] == status]
    
    if type:
        projects = [p for p in projects if p["type"] == type]
    
    if client_id:
        projects = [p for p in projects if p["client_id"] == client_id]
    
    total = len(projects)
    start = (page - 1) * limit
    end = start + limit
    projects = projects[start:end]
    
    for project in projects:
        client = db.clients.get(project["client_id"])
        project["client_name"] = client["name"] if client else "غير محدد"
    
    return {
        "projects": projects,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    }

@router.get("/{project_id}", response_model=Project)
async def get_project(
    project_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    project = db.projects.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="المشروع غير موجود")
    
    client = db.clients.get(project["client_id"])
    project["client_name"] = client["name"] if client else "غير محدد"
    
    return project

@router.post("/", response_model=Project)
async def create_project(
    project_data: ProjectCreate,
    current_user: dict = Depends(get_current_active_user)
):
    if project_data.client_id not in db.clients:
        raise HTTPException(status_code=400, detail="العميل غير موجود")
    
    project_id = db._get_next_id('projects')
    now = datetime.now()
    
    project = {
        "id": project_id,
        **project_data.dict(),
        "actual_hours": 0.0,
        "actual_cost": 0.0,
        "progress": 0.0,
        "files": [],
        "milestones": [],
        "risks": [],
        "created_at": now,
        "updated_at": now
    }
    
    db.projects[project_id] = project
    
    client = db.clients[project_data.client_id]
    client["total_projects"] += 1
    client["last_project_date"] = now
    db.clients[project_data.client_id] = client
    
    return project

@router.put("/{project_id}", response_model=Project)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    current_user: dict = Depends(get_current_active_user)
):
    project = db.projects.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="المشروع غير موجود")
    
    update_data = project_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        project[key] = value
    
    project["updated_at"] = datetime.now()
    db.projects[project_id] = project
    return project

@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    if project_id not in db.projects:
        raise HTTPException(status_code=404, detail="المشروع غير موجود")
    
    del db.projects[project_id]
    return {"message": "تم حذف المشروع بنجاح"}

@router.get("/{project_id}/tasks")
async def get_project_tasks(
    project_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    if project_id not in db.projects:
        raise HTTPException(status_code=404, detail="المشروع غير موجود")
    
    tasks = [t for t in db.tasks.values() if t.get("project_id") == project_id]
    return {"tasks": tasks}

@router.get("/{project_id}/transactions")
async def get_project_transactions(
    project_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    if project_id not in db.projects:
        raise HTTPException(status_code=404, detail="المشروع غير موجود")
    
    transactions = [t for t in db.transactions.values() if t.get("project_id") == project_id]
    return {"transactions": transactions}

@router.post("/{project_id}/clone")
async def clone_project(
    project_id: int,
    new_name: str,
    current_user: dict = Depends(get_current_active_user)
):
    original_project = db.projects.get(project_id)
    if not original_project:
        raise HTTPException(status_code=404, detail="المشروع غير موجود")
    
    new_project_id = db._get_next_id('projects')
    now = datetime.now()
    
    cloned_project = original_project.copy()
    cloned_project.update({
        "id": new_project_id,
        "name": new_name,
        "status": "planning",
        "progress": 0.0,
        "actual_hours": 0.0,
        "actual_cost": 0.0,
        "start_date": None,
        "end_date": None,
        "created_at": now,
        "updated_at": now
    })
    
    db.projects[new_project_id] = cloned_project
    return cloned_project

@router.get("/stats/overview")
async def get_projects_stats(current_user: dict = Depends(get_current_active_user)):
    projects = list(db.projects.values())
    total_projects = len(projects)
    active_projects = len([p for p in projects if p["status"] == "in_progress"])
    completed_projects = len([p for p in projects if p["status"] == "completed"])
    total_budget = sum(p.get("budget", 0) for p in projects if p.get("budget"))
    total_actual_cost = sum(p.get("actual_cost", 0) for p in projects)
    
    return {
        "total_projects": total_projects,
        "active_projects": active_projects,
        "completed_projects": completed_projects,
        "total_budget": total_budget,
        "total_actual_cost": total_actual_cost,
        "budget_utilization": (total_actual_cost / total_budget * 100) if total_budget > 0 else 0
    }
