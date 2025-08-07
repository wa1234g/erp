from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional, Dict
from datetime import datetime
from ..models.task import Task, TaskCreate, TaskUpdate, KanbanMove, TaskStatus
from ..database import db
from ..auth.dependencies import get_current_active_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/", response_model=dict)
async def get_tasks(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    assigned_to: Optional[int] = None,
    project_id: Optional[int] = None,
    current_user: dict = Depends(get_current_active_user)
):
    tasks = list(db.tasks.values())
    
    if search:
        tasks = [t for t in tasks if search.lower() in t["title"].lower()]
    
    if status:
        tasks = [t for t in tasks if t["status"] == status]
    
    if priority:
        tasks = [t for t in tasks if t["priority"] == priority]
    
    if assigned_to:
        tasks = [t for t in tasks if t.get("assigned_to") == assigned_to]
    
    if project_id:
        tasks = [t for t in tasks if t.get("project_id") == project_id]
    
    total = len(tasks)
    start = (page - 1) * limit
    end = start + limit
    tasks = tasks[start:end]
    
    for task in tasks:
        if task.get("assigned_to"):
            user = db.users.get(task["assigned_to"])
            task["assigned_user_name"] = user["full_name"] if user else "غير محدد"
        
        if task.get("project_id"):
            project = db.projects.get(task["project_id"])
            task["project_name"] = project["name"] if project else "غير محدد"
    
    return {
        "tasks": tasks,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    }

@router.get("/kanban")
async def get_kanban_board(
    project_id: Optional[int] = None,
    current_user: dict = Depends(get_current_active_user)
):
    tasks = list(db.tasks.values())
    
    if project_id:
        tasks = [t for t in tasks if t.get("project_id") == project_id]
    
    kanban_board = {
        "todo": [],
        "in_progress": [],
        "in_review": [],
        "done": []
    }
    
    for task in tasks:
        status = task["status"]
        if status in kanban_board:
            if task.get("assigned_to"):
                user = db.users.get(task["assigned_to"])
                task["assigned_user_name"] = user["full_name"] if user else "غير محدد"
            kanban_board[status].append(task)
    
    for status in kanban_board:
        kanban_board[status].sort(key=lambda x: x["kanban_position"])
    
    return kanban_board

@router.post("/kanban/move")
async def move_task_kanban(
    move_data: KanbanMove,
    current_user: dict = Depends(get_current_active_user)
):
    task = db.tasks.get(move_data.task_id)
    if not task:
        raise HTTPException(status_code=404, detail="المهمة غير موجودة")
    
    task["status"] = move_data.new_status
    task["kanban_position"] = move_data.new_position
    task["updated_at"] = datetime.now()
    
    if move_data.new_status == TaskStatus.DONE and not task.get("completed_at"):
        task["completed_at"] = datetime.now()
    elif move_data.new_status != TaskStatus.DONE:
        task["completed_at"] = None
    
    db.tasks[move_data.task_id] = task
    return {"message": "تم نقل المهمة بنجاح"}

@router.get("/{task_id}", response_model=Task)
async def get_task(
    task_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    task = db.tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="المهمة غير موجودة")
    
    if task.get("assigned_to"):
        user = db.users.get(task["assigned_to"])
        task["assigned_user_name"] = user["full_name"] if user else "غير محدد"
    
    if task.get("project_id"):
        project = db.projects.get(task["project_id"])
        task["project_name"] = project["name"] if project else "غير محدد"
    
    return task

@router.post("/", response_model=Task)
async def create_task(
    task_data: TaskCreate,
    current_user: dict = Depends(get_current_active_user)
):
    if task_data.project_id and task_data.project_id not in db.projects:
        raise HTTPException(status_code=400, detail="المشروع غير موجود")
    
    if task_data.assigned_to and task_data.assigned_to not in db.users:
        raise HTTPException(status_code=400, detail="المستخدم المعين غير موجود")
    
    task_id = db._get_next_id('tasks')
    now = datetime.now()
    
    task = {
        "id": task_id,
        **task_data.dict(),
        "created_by": current_user["id"],
        "actual_hours": 0.0,
        "completed_at": None,
        "attachments": [],
        "comments": [],
        "time_entries": [],
        "created_at": now,
        "updated_at": now
    }
    
    db.tasks[task_id] = task
    return task

@router.put("/{task_id}", response_model=Task)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: dict = Depends(get_current_active_user)
):
    task = db.tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="المهمة غير موجودة")
    
    update_data = task_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        task[key] = value
    
    if update_data.get("status") == "done" and not task.get("completed_at"):
        task["completed_at"] = datetime.now()
    elif update_data.get("status") != "done":
        task["completed_at"] = None
    
    task["updated_at"] = datetime.now()
    db.tasks[task_id] = task
    return task

@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    if task_id not in db.tasks:
        raise HTTPException(status_code=404, detail="المهمة غير موجودة")
    
    del db.tasks[task_id]
    return {"message": "تم حذف المهمة بنجاح"}

@router.post("/bulk-delete")
async def bulk_delete_tasks(
    task_ids: List[int],
    current_user: dict = Depends(get_current_active_user)
):
    deleted_count = 0
    for task_id in task_ids:
        if task_id in db.tasks:
            del db.tasks[task_id]
            deleted_count += 1
    
    return {"message": f"تم حذف {deleted_count} مهمة بنجاح"}

@router.post("/{task_id}/comments")
async def add_task_comment(
    task_id: int,
    content: str,
    current_user: dict = Depends(get_current_active_user)
):
    task = db.tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="المهمة غير موجودة")
    
    comment = {
        "id": len(task["comments"]) + 1,
        "user_id": current_user["id"],
        "content": content,
        "attachments": [],
        "created_at": datetime.now(),
        "updated_at": None
    }
    
    task["comments"].append(comment)
    task["updated_at"] = datetime.now()
    db.tasks[task_id] = task
    
    return comment

@router.get("/stats/overview")
async def get_tasks_stats(current_user: dict = Depends(get_current_active_user)):
    tasks = list(db.tasks.values())
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t["status"] == "done"])
    in_progress_tasks = len([t for t in tasks if t["status"] == "in_progress"])
    overdue_tasks = len([t for t in tasks if t.get("due_date") and 
                        datetime.fromisoformat(t["due_date"].replace('Z', '+00:00')) < datetime.now() and 
                        t["status"] != "done"])
    
    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "in_progress_tasks": in_progress_tasks,
        "overdue_tasks": overdue_tasks,
        "completion_rate": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    }
