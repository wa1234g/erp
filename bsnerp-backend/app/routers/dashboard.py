from fastapi import APIRouter, Depends
from datetime import datetime, timedelta
from ..database import db
from ..auth.dependencies import get_current_active_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats")
async def get_dashboard_stats(current_user: dict = Depends(get_current_active_user)):
    now = datetime.now()
    
    clients = list(db.clients.values())
    projects = list(db.projects.values())
    tasks = list(db.tasks.values())
    transactions = list(db.transactions.values())
    servers = list(db.servers.values())
    
    total_clients = len(clients)
    active_clients = len([c for c in clients if c["status"] == "active"])
    
    total_projects = len(projects)
    active_projects = len([p for p in projects if p["status"] == "in_progress"])
    completed_projects = len([p for p in projects if p["status"] == "completed"])
    
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t["status"] == "done"])
    overdue_tasks = len([t for t in tasks if t.get("due_date") and 
                        datetime.fromisoformat(t["due_date"].replace('Z', '+00:00')) < now and 
                        t["status"] != "done"])
    
    approved_transactions = [t for t in transactions if t["status"] == "approved"]
    total_revenue = sum(t["amount"] for t in approved_transactions if t["type"] == "income")
    total_expenses = sum(t["amount"] for t in approved_transactions if t["type"] == "expense")
    net_profit = total_revenue - total_expenses
    
    online_servers = len([s for s in servers if s["status"] == "online"])
    offline_servers = len([s for s in servers if s["status"] == "offline"])
    
    return {
        "clients": {
            "total": total_clients,
            "active": active_clients,
            "growth": 12.5
        },
        "projects": {
            "total": total_projects,
            "active": active_projects,
            "completed": completed_projects,
            "completion_rate": (completed_projects / total_projects * 100) if total_projects > 0 else 0
        },
        "tasks": {
            "total": total_tasks,
            "completed": completed_tasks,
            "overdue": overdue_tasks,
            "completion_rate": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        },
        "finance": {
            "revenue": total_revenue,
            "expenses": total_expenses,
            "profit": net_profit,
            "profit_margin": (net_profit / total_revenue * 100) if total_revenue > 0 else 0
        },
        "servers": {
            "total": len(servers),
            "online": online_servers,
            "offline": offline_servers,
            "uptime": (online_servers / len(servers) * 100) if len(servers) > 0 else 0
        }
    }

@router.get("/recent-activity")
async def get_recent_activity(current_user: dict = Depends(get_current_active_user)):
    activities = []
    
    recent_projects = sorted(db.projects.values(), key=lambda x: x["created_at"], reverse=True)[:5]
    for project in recent_projects:
        client = db.clients.get(project["client_id"])
        activities.append({
            "type": "project_created",
            "title": f"مشروع جديد: {project['name']}",
            "description": f"تم إنشاء مشروع جديد للعميل {client['name'] if client else 'غير محدد'}",
            "timestamp": project["created_at"],
            "icon": "folder-plus"
        })
    
    recent_tasks = sorted(db.tasks.values(), key=lambda x: x["created_at"], reverse=True)[:5]
    for task in recent_tasks:
        activities.append({
            "type": "task_created",
            "title": f"مهمة جديدة: {task['title']}",
            "description": f"تم إنشاء مهمة جديدة بأولوية {task['priority']}",
            "timestamp": task["created_at"],
            "icon": "check-square"
        })
    
    recent_transactions = sorted(db.transactions.values(), key=lambda x: x["created_at"], reverse=True)[:5]
    for transaction in recent_transactions:
        activities.append({
            "type": "transaction_created",
            "title": f"معاملة مالية: {transaction['description']}",
            "description": f"{transaction['amount']} {transaction['currency']} - {transaction['type']}",
            "timestamp": transaction["created_at"],
            "icon": "dollar-sign"
        })
    
    activities.sort(key=lambda x: x["timestamp"], reverse=True)
    return {"activities": activities[:10]}

@router.get("/charts/revenue")
async def get_revenue_chart(current_user: dict = Depends(get_current_active_user)):
    from datetime import datetime, timedelta
    import calendar
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    transactions = [t for t in db.transactions.values() if 
                   datetime.fromisoformat(t["transaction_date"].replace('Z', '+00:00')) >= start_date and
                   t["status"] == "approved"]
    
    monthly_data = {}
    for i in range(12):
        month_start = end_date - timedelta(days=(12 - i) * 30)
        month_end = end_date - timedelta(days=(12 - i - 1) * 30)
        month_key = month_start.strftime("%Y-%m")
        
        month_transactions = [t for t in transactions if 
                            month_start <= datetime.fromisoformat(t["transaction_date"].replace('Z', '+00:00')) < month_end]
        
        revenue = sum(t["amount"] for t in month_transactions if t["type"] == "income")
        expenses = sum(t["amount"] for t in month_transactions if t["type"] == "expense")
        
        monthly_data[month_key] = {
            "month": month_start.strftime("%b"),
            "revenue": revenue,
            "expenses": expenses,
            "profit": revenue - expenses
        }
    
    return {"data": list(monthly_data.values())}

@router.get("/charts/projects")
async def get_projects_chart(current_user: dict = Depends(get_current_active_user)):
    projects = list(db.projects.values())
    
    status_counts = {}
    for project in projects:
        status = project["status"]
        status_counts[status] = status_counts.get(status, 0) + 1
    
    chart_data = []
    status_labels = {
        "planning": "تخطيط",
        "in_progress": "قيد التنفيذ",
        "on_hold": "متوقف",
        "completed": "مكتمل",
        "cancelled": "ملغي"
    }
    
    for status, count in status_counts.items():
        chart_data.append({
            "name": status_labels.get(status, status),
            "value": count,
            "status": status
        })
    
    return {"data": chart_data}

@router.get("/charts/tasks")
async def get_tasks_chart(current_user: dict = Depends(get_current_active_user)):
    tasks = list(db.tasks.values())
    
    priority_counts = {}
    for task in tasks:
        priority = task["priority"]
        priority_counts[priority] = priority_counts.get(priority, 0) + 1
    
    chart_data = []
    priority_labels = {
        "low": "منخفضة",
        "medium": "متوسطة", 
        "high": "عالية",
        "urgent": "عاجلة"
    }
    
    for priority, count in priority_counts.items():
        chart_data.append({
            "name": priority_labels.get(priority, priority),
            "value": count,
            "priority": priority
        })
    
    return {"data": chart_data}
