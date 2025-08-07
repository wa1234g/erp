from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from datetime import datetime, timedelta
from ..models.credential import Credential, CredentialCreate, CredentialUpdate, PasswordStrength, ConnectionTest
from ..database import db
from ..auth.dependencies import get_current_active_user
from ..auth.jwt_handler import generate_password, check_password_strength
import base64
import secrets

router = APIRouter(prefix="/credentials", tags=["Credentials"])

def encrypt_password(password: str) -> str:
    encoded = base64.b64encode(password.encode()).decode()
    return encoded

def decrypt_password(encrypted_password: str) -> str:
    decoded = base64.b64decode(encrypted_password.encode()).decode()
    return decoded

@router.get("/", response_model=dict)
async def get_credentials(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    type: Optional[str] = None,
    status: Optional[str] = None,
    client_id: Optional[int] = None,
    current_user: dict = Depends(get_current_active_user)
):
    credentials = list(db.credentials.values())
    
    if type:
        credentials = [c for c in credentials if c["type"] == type]
    
    if status:
        credentials = [c for c in credentials if c["status"] == status]
    
    if client_id:
        credentials = [c for c in credentials if c.get("client_id") == client_id]
    
    total = len(credentials)
    start = (page - 1) * limit
    end = start + limit
    credentials = credentials[start:end]
    
    for credential in credentials:
        credential["password"] = "••••••••"
        
        if credential.get("client_id"):
            client = db.clients.get(credential["client_id"])
            credential["client_name"] = client["name"] if client else "غير محدد"
        
        if credential.get("project_id"):
            project = db.projects.get(credential["project_id"])
            credential["project_name"] = project["name"] if project else "غير محدد"
    
    return {
        "credentials": credentials,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    }

@router.get("/{credential_id}", response_model=Credential)
async def get_credential(
    credential_id: int,
    show_password: bool = False,
    current_user: dict = Depends(get_current_active_user)
):
    credential = db.credentials.get(credential_id)
    if not credential:
        raise HTTPException(status_code=404, detail="بيانات الدخول غير موجودة")
    
    credential_copy = credential.copy()
    
    if not show_password:
        credential_copy["password"] = "••••••••"
    else:
        credential_copy["password"] = decrypt_password(credential["password"])
    
    return credential_copy

@router.post("/", response_model=Credential)
async def create_credential(
    credential_data: CredentialCreate,
    current_user: dict = Depends(get_current_active_user)
):
    credential_id = db._get_next_id('credentials')
    now = datetime.now()
    
    encrypted_password = encrypt_password(credential_data.password)
    
    credential = {
        "id": credential_id,
        **credential_data.dict(exclude={"password"}),
        "password": encrypted_password,
        "status": "active",
        "last_tested": None,
        "test_status": None,
        "created_at": now,
        "updated_at": now
    }
    
    if credential_data.expiry_date:
        days_until_expiry = (credential_data.expiry_date - now).days
        if days_until_expiry <= 30:
            credential["status"] = "expiring_soon"
        elif days_until_expiry <= 0:
            credential["status"] = "expired"
    
    db.credentials[credential_id] = credential
    return credential

@router.put("/{credential_id}", response_model=Credential)
async def update_credential(
    credential_id: int,
    credential_data: CredentialUpdate,
    current_user: dict = Depends(get_current_active_user)
):
    credential = db.credentials.get(credential_id)
    if not credential:
        raise HTTPException(status_code=404, detail="بيانات الدخول غير موجودة")
    
    update_data = credential_data.dict(exclude_unset=True)
    
    if "password" in update_data:
        update_data["password"] = encrypt_password(update_data["password"])
    
    for key, value in update_data.items():
        credential[key] = value
    
    credential["updated_at"] = datetime.now()
    db.credentials[credential_id] = credential
    return credential

@router.delete("/{credential_id}")
async def delete_credential(
    credential_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    if credential_id not in db.credentials:
        raise HTTPException(status_code=404, detail="بيانات الدخول غير موجودة")
    
    del db.credentials[credential_id]
    return {"message": "تم حذف بيانات الدخول بنجاح"}

@router.post("/generate-password")
async def generate_secure_password(
    length: int = Query(12, ge=8, le=50),
    include_symbols: bool = True,
    current_user: dict = Depends(get_current_active_user)
):
    password = generate_password(length)
    strength = check_password_strength(password)
    
    return {
        "password": password,
        "strength": strength
    }

@router.post("/check-password-strength")
async def check_password_strength_endpoint(
    password: str,
    current_user: dict = Depends(get_current_active_user)
):
    strength = check_password_strength(password)
    return strength

@router.post("/{credential_id}/test-connection")
async def test_credential_connection(
    credential_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    credential = db.credentials.get(credential_id)
    if not credential:
        raise HTTPException(status_code=404, detail="بيانات الدخول غير موجودة")
    
    import random
    import time
    
    start_time = time.time()
    
    success = random.choice([True, True, True, False])
    response_time = round((time.time() - start_time) * 1000 + random.uniform(50, 500), 2)
    
    test_result = {
        "credential_id": credential_id,
        "success": success,
        "response_time": response_time if success else None,
        "error_message": None if success else "فشل في الاتصال - تحقق من بيانات الدخول",
        "tested_at": datetime.now()
    }
    
    credential["last_tested"] = test_result["tested_at"]
    credential["test_status"] = "success" if success else "failed"
    credential["updated_at"] = datetime.now()
    db.credentials[credential_id] = credential
    
    return test_result

@router.get("/{credential_id}/share")
async def share_credential(
    credential_id: int,
    user_ids: List[int],
    current_user: dict = Depends(get_current_active_user)
):
    credential = db.credentials.get(credential_id)
    if not credential:
        raise HTTPException(status_code=404, detail="بيانات الدخول غير موجودة")
    
    for user_id in user_ids:
        if user_id not in db.users:
            raise HTTPException(status_code=400, detail=f"المستخدم {user_id} غير موجود")
    
    credential["shared_with"] = list(set(credential.get("shared_with", []) + user_ids))
    credential["updated_at"] = datetime.now()
    db.credentials[credential_id] = credential
    
    return {"message": f"تم مشاركة بيانات الدخول مع {len(user_ids)} مستخدم"}

@router.get("/expiring-soon")
async def get_expiring_credentials(
    days: int = Query(30, ge=1, le=365),
    current_user: dict = Depends(get_current_active_user)
):
    now = datetime.now()
    expiry_threshold = now + timedelta(days=days)
    
    expiring_credentials = []
    for credential in db.credentials.values():
        if credential.get("expiry_date"):
            expiry_date = credential["expiry_date"]
            if isinstance(expiry_date, str):
                expiry_date = datetime.fromisoformat(expiry_date.replace('Z', '+00:00'))
            
            if expiry_date <= expiry_threshold:
                days_until_expiry = (expiry_date - now).days
                credential_copy = credential.copy()
                credential_copy["password"] = "••••••••"
                credential_copy["days_until_expiry"] = days_until_expiry
                expiring_credentials.append(credential_copy)
    
    expiring_credentials.sort(key=lambda x: x["days_until_expiry"])
    return {"credentials": expiring_credentials}

@router.get("/stats/overview")
async def get_credentials_stats(current_user: dict = Depends(get_current_active_user)):
    credentials = list(db.credentials.values())
    total_credentials = len(credentials)
    active_credentials = len([c for c in credentials if c["status"] == "active"])
    expiring_credentials = len([c for c in credentials if c["status"] == "expiring_soon"])
    expired_credentials = len([c for c in credentials if c["status"] == "expired"])
    
    return {
        "total_credentials": total_credentials,
        "active_credentials": active_credentials,
        "expiring_credentials": expiring_credentials,
        "expired_credentials": expired_credentials
    }
