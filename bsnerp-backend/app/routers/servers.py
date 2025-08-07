from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from datetime import datetime
from ..models.server import Server, ServerCreate, ServerUpdate, BackupRecord, MaintenanceRecord
from ..database import db
from ..auth.dependencies import get_current_active_user

router = APIRouter(prefix="/servers", tags=["Servers"])

@router.get("/", response_model=dict)
async def get_servers(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[str] = None,
    type: Optional[str] = None,
    current_user: dict = Depends(get_current_active_user)
):
    servers = list(db.servers.values())
    
    if status:
        servers = [s for s in servers if s["status"] == status]
    
    if type:
        servers = [s for s in servers if s["type"] == type]
    
    total = len(servers)
    start = (page - 1) * limit
    end = start + limit
    servers = servers[start:end]
    
    return {
        "servers": servers,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    }

@router.get("/{server_id}", response_model=Server)
async def get_server(
    server_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    server = db.servers.get(server_id)
    if not server:
        raise HTTPException(status_code=404, detail="الخادم غير موجود")
    return server

@router.post("/", response_model=Server)
async def create_server(
    server_data: ServerCreate,
    current_user: dict = Depends(get_current_active_user)
):
    server_id = db._get_next_id('servers')
    now = datetime.now()
    
    server = {
        "id": server_id,
        **server_data.dict(),
        "status": "online",
        "last_backup": None,
        "uptime_percentage": 100.0,
        "cpu_usage": 0.0,
        "memory_usage": 0.0,
        "disk_usage": 0.0,
        "network_in": 0.0,
        "network_out": 0.0,
        "installed_software": [],
        "security_updates": [],
        "ssl_certificates": [],
        "projects": [],
        "created_at": now,
        "updated_at": now
    }
    
    db.servers[server_id] = server
    return server

@router.put("/{server_id}", response_model=Server)
async def update_server(
    server_id: int,
    server_data: ServerUpdate,
    current_user: dict = Depends(get_current_active_user)
):
    server = db.servers.get(server_id)
    if not server:
        raise HTTPException(status_code=404, detail="الخادم غير موجود")
    
    update_data = server_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        server[key] = value
    
    server["updated_at"] = datetime.now()
    db.servers[server_id] = server
    return server

@router.delete("/{server_id}")
async def delete_server(
    server_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    if server_id not in db.servers:
        raise HTTPException(status_code=404, detail="الخادم غير موجود")
    
    del db.servers[server_id]
    return {"message": "تم حذف الخادم بنجاح"}

@router.get("/{server_id}/monitoring")
async def get_server_monitoring(
    server_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    server = db.servers.get(server_id)
    if not server:
        raise HTTPException(status_code=404, detail="الخادم غير موجود")
    
    import random
    
    monitoring_data = {
        "cpu_usage": round(random.uniform(10, 90), 1),
        "memory_usage": round(random.uniform(20, 80), 1),
        "disk_usage": round(random.uniform(15, 75), 1),
        "network_in": round(random.uniform(100, 2000), 1),
        "network_out": round(random.uniform(200, 3000), 1),
        "uptime": round(random.uniform(95, 100), 2),
        "response_time": round(random.uniform(50, 200), 0),
        "last_updated": datetime.now()
    }
    
    server.update(monitoring_data)
    db.servers[server_id] = server
    
    return monitoring_data

@router.post("/{server_id}/backup")
async def create_backup(
    server_id: int,
    backup_type: str = "full",
    current_user: dict = Depends(get_current_active_user)
):
    server = db.servers.get(server_id)
    if not server:
        raise HTTPException(status_code=404, detail="الخادم غير موجود")
    
    backup_id = db._get_next_id('backup_records')
    now = datetime.now()
    
    backup = {
        "id": backup_id,
        "server_id": server_id,
        "backup_type": backup_type,
        "status": "in_progress",
        "file_path": f"/backups/{server['name']}-{now.strftime('%Y%m%d-%H%M%S')}.tar.gz",
        "file_size": None,
        "started_at": now,
        "completed_at": None,
        "error_message": None
    }
    
    db.backup_records[backup_id] = backup
    
    import random
    import time
    if random.choice([True, False]):
        backup["status"] = "success"
        backup["completed_at"] = now
        backup["file_size"] = random.randint(1000000, 10000000)
        server["last_backup"] = now
    else:
        backup["status"] = "failed"
        backup["error_message"] = "فشل في الاتصال بالخادم"
    
    db.backup_records[backup_id] = backup
    db.servers[server_id] = server
    
    return backup

@router.get("/{server_id}/backups")
async def get_server_backups(
    server_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    if server_id not in db.servers:
        raise HTTPException(status_code=404, detail="الخادم غير موجود")
    
    backups = [b for b in db.backup_records.values() if b["server_id"] == server_id]
    backups.sort(key=lambda x: x["started_at"], reverse=True)
    
    return {"backups": backups}

@router.post("/{server_id}/maintenance")
async def schedule_maintenance(
    server_id: int,
    title: str,
    description: str,
    scheduled_start: datetime,
    scheduled_end: datetime,
    current_user: dict = Depends(get_current_active_user)
):
    server = db.servers.get(server_id)
    if not server:
        raise HTTPException(status_code=404, detail="الخادم غير موجود")
    
    maintenance_id = db._get_next_id('maintenance_records')
    
    maintenance = {
        "id": maintenance_id,
        "server_id": server_id,
        "title": title,
        "description": description,
        "status": "scheduled",
        "scheduled_start": scheduled_start,
        "scheduled_end": scheduled_end,
        "actual_start": None,
        "actual_end": None,
        "performed_by": current_user["id"],
        "notes": None
    }
    
    db.maintenance_records[maintenance_id] = maintenance
    return maintenance

@router.get("/stats/overview")
async def get_servers_stats(current_user: dict = Depends(get_current_active_user)):
    servers = list(db.servers.values())
    total_servers = len(servers)
    online_servers = len([s for s in servers if s["status"] == "online"])
    offline_servers = len([s for s in servers if s["status"] == "offline"])
    maintenance_servers = len([s for s in servers if s["status"] == "maintenance"])
    
    total_monthly_cost = sum(s.get("monthly_cost", 0) for s in servers)
    avg_uptime = sum(s.get("uptime_percentage", 0) for s in servers) / total_servers if total_servers > 0 else 0
    
    return {
        "total_servers": total_servers,
        "online_servers": online_servers,
        "offline_servers": offline_servers,
        "maintenance_servers": maintenance_servers,
        "total_monthly_cost": total_monthly_cost,
        "average_uptime": round(avg_uptime, 2)
    }
