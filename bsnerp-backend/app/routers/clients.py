from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from datetime import datetime
from ..models.client import Client, ClientCreate, ClientUpdate, ClientFilter
from ..database import db
from ..auth.dependencies import get_current_active_user

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.get("/", response_model=dict)
async def get_clients(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    status: Optional[str] = None,
    type: Optional[str] = None,
    current_user: dict = Depends(get_current_active_user)
):
    clients = list(db.clients.values())
    
    if search:
        clients = [c for c in clients if 
                  search.lower() in c["name"].lower() or 
                  search.lower() in c["email"].lower() or
                  (c["company_name"] and search.lower() in c["company_name"].lower())]
    
    if status:
        clients = [c for c in clients if c["status"] == status]
    
    if type:
        clients = [c for c in clients if c["type"] == type]
    
    total = len(clients)
    start = (page - 1) * limit
    end = start + limit
    clients = clients[start:end]
    
    return {
        "clients": clients,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    }

@router.get("/{client_id}", response_model=Client)
async def get_client(
    client_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    client = db.clients.get(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="العميل غير موجود")
    return client

@router.post("/", response_model=Client)
async def create_client(
    client_data: ClientCreate,
    current_user: dict = Depends(get_current_active_user)
):
    client_id = db._get_next_id('clients')
    now = datetime.now()
    
    client = {
        "id": client_id,
        **client_data.dict(),
        "total_projects": 0,
        "total_revenue": 0.0,
        "last_project_date": None,
        "documents": [],
        "created_at": now,
        "updated_at": now
    }
    
    db.clients[client_id] = client
    return client

@router.put("/{client_id}", response_model=Client)
async def update_client(
    client_id: int,
    client_data: ClientUpdate,
    current_user: dict = Depends(get_current_active_user)
):
    client = db.clients.get(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="العميل غير موجود")
    
    update_data = client_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        client[key] = value
    
    client["updated_at"] = datetime.now()
    db.clients[client_id] = client
    return client

@router.delete("/{client_id}")
async def delete_client(
    client_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    if client_id not in db.clients:
        raise HTTPException(status_code=404, detail="العميل غير موجود")
    
    del db.clients[client_id]
    return {"message": "تم حذف العميل بنجاح"}

@router.post("/bulk-delete")
async def bulk_delete_clients(
    client_ids: List[int],
    current_user: dict = Depends(get_current_active_user)
):
    deleted_count = 0
    for client_id in client_ids:
        if client_id in db.clients:
            del db.clients[client_id]
            deleted_count += 1
    
    return {"message": f"تم حذف {deleted_count} عميل بنجاح"}

@router.get("/{client_id}/projects")
async def get_client_projects(
    client_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    if client_id not in db.clients:
        raise HTTPException(status_code=404, detail="العميل غير موجود")
    
    projects = [p for p in db.projects.values() if p["client_id"] == client_id]
    return {"projects": projects}

@router.get("/{client_id}/transactions")
async def get_client_transactions(
    client_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    if client_id not in db.clients:
        raise HTTPException(status_code=404, detail="العميل غير موجود")
    
    transactions = [t for t in db.transactions.values() if t.get("client_id") == client_id]
    return {"transactions": transactions}

@router.get("/stats/overview")
async def get_clients_stats(current_user: dict = Depends(get_current_active_user)):
    clients = list(db.clients.values())
    total_clients = len(clients)
    active_clients = len([c for c in clients if c["status"] == "active"])
    total_revenue = sum(c["total_revenue"] for c in clients)
    
    return {
        "total_clients": total_clients,
        "active_clients": active_clients,
        "total_revenue": total_revenue,
        "average_revenue": total_revenue / total_clients if total_clients > 0 else 0
    }
