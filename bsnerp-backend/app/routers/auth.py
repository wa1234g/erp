from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from datetime import datetime, timedelta
from typing import Dict, Any
from ..models.user import UserLogin, PasswordReset, PasswordResetConfirm, TwoFactorSetup
from ..database import db
from ..auth.jwt_handler import (
    verify_password, create_access_token, create_refresh_token, verify_token,
    generate_reset_token, generate_2fa_secret, verify_2fa_code, generate_2fa_qr_code
)
from ..auth.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()

@router.post("/login")
async def login(user_credentials: UserLogin):
    user = None
    for u in db.users.values():
        if u["email"] == user_credentials.email:
            user = u
            break
    
    if not user or not verify_password(user_credentials.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="البريد الإلكتروني أو كلمة المرور غير صحيحة"
        )
    
    if user["status"] != "active":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="الحساب غير مفعل"
        )
    
    if user["two_factor_enabled"]:
        if not user_credentials.two_factor_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="مطلوب رمز التحقق الثنائي"
            )
        
        if not verify_2fa_code(user["two_factor_secret"], user_credentials.two_factor_code):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="رمز التحقق الثنائي غير صحيح"
            )
    
    access_token_expires = timedelta(minutes=30)
    if user_credentials.remember_me:
        access_token_expires = timedelta(days=7)
    
    access_token = create_access_token(
        data={"sub": user["id"], "email": user["email"], "role": user["role"]},
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": user["id"], "email": user["email"]}
    )
    
    user["last_login"] = datetime.now()
    db.users[user["id"]] = user
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "email": user["email"],
            "full_name": user["full_name"],
            "role": user["role"],
            "avatar": user["avatar"]
        }
    }

@router.post("/refresh")
async def refresh_token(refresh_token: str):
    payload = verify_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user_id = payload.get("sub")
    user = db.users.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    access_token = create_access_token(
        data={"sub": user["id"], "email": user["email"], "role": user["role"]}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/password-reset")
async def request_password_reset(reset_request: PasswordReset):
    user = None
    for u in db.users.values():
        if u["email"] == reset_request.email:
            user = u
            break
    
    if not user:
        return {"message": "إذا كان البريد الإلكتروني موجود، ستصلك رسالة إعادة تعيين كلمة المرور"}
    
    reset_token = generate_reset_token()
    user["reset_token"] = reset_token
    user["reset_token_expires"] = datetime.now() + timedelta(hours=1)
    db.users[user["id"]] = user
    
    return {"message": "تم إرسال رابط إعادة تعيين كلمة المرور إلى بريدك الإلكتروني"}

@router.post("/password-reset/confirm")
async def confirm_password_reset(reset_data: PasswordResetConfirm):
    user = None
    for u in db.users.values():
        if u.get("reset_token") == reset_data.token:
            user = u
            break
    
    if not user or not user.get("reset_token_expires") or user["reset_token_expires"] < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="رمز إعادة التعيين غير صالح أو منتهي الصلاحية"
        )
    
    from ..auth.jwt_handler import get_password_hash
    user["password_hash"] = get_password_hash(reset_data.new_password)
    user["reset_token"] = None
    user["reset_token_expires"] = None
    user["updated_at"] = datetime.now()
    db.users[user["id"]] = user
    
    return {"message": "تم تغيير كلمة المرور بنجاح"}

@router.post("/2fa/setup")
async def setup_2fa(current_user: dict = Depends(get_current_user)):
    secret = generate_2fa_secret()
    qr_code = generate_2fa_qr_code(secret, current_user["email"])
    
    return {
        "secret": secret,
        "qr_code": qr_code,
        "backup_codes": [generate_reset_token()[:8] for _ in range(10)]
    }

@router.post("/2fa/enable")
async def enable_2fa(setup_data: TwoFactorSetup, current_user: dict = Depends(get_current_user)):
    if not verify_2fa_code(setup_data.secret, setup_data.code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="رمز التحقق غير صحيح"
        )
    
    current_user["two_factor_enabled"] = True
    current_user["two_factor_secret"] = setup_data.secret
    current_user["updated_at"] = datetime.now()
    db.users[current_user["id"]] = current_user
    
    return {"message": "تم تفعيل التحقق الثنائي بنجاح"}

@router.post("/2fa/disable")
async def disable_2fa(current_user: dict = Depends(get_current_user)):
    current_user["two_factor_enabled"] = False
    current_user["two_factor_secret"] = None
    current_user["updated_at"] = datetime.now()
    db.users[current_user["id"]] = current_user
    
    return {"message": "تم إلغاء التحقق الثنائي بنجاح"}

@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "username": current_user["username"],
        "full_name": current_user["full_name"],
        "phone": current_user["phone"],
        "role": current_user["role"],
        "status": current_user["status"],
        "avatar": current_user["avatar"],
        "department": current_user["department"],
        "position": current_user["position"],
        "skills": current_user["skills"],
        "permissions": current_user["permissions"],
        "two_factor_enabled": current_user["two_factor_enabled"],
        "last_login": current_user["last_login"],
        "email_verified": current_user["email_verified"]
    }
