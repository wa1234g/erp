from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
import secrets
import pyotp
from io import BytesIO
import base64

SECRET_KEY = "bsnerp-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: Dict[str, Any]) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def generate_reset_token() -> str:
    return secrets.token_urlsafe(32)

def generate_verification_token() -> str:
    return secrets.token_urlsafe(32)

def generate_2fa_secret() -> str:
    return pyotp.random_base32()

def verify_2fa_code(secret: str, code: str) -> bool:
    totp = pyotp.TOTP(secret)
    return totp.verify(code, valid_window=1)

def generate_2fa_qr_code(secret: str, user_email: str) -> str:
    totp = pyotp.TOTP(secret)
    provisioning_uri = totp.provisioning_uri(
        name=user_email,
        issuer_name="BSN ERP"
    )
    
    try:
        import qrcode
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"
    except ImportError:
        return provisioning_uri

def generate_password(length: int = 12) -> str:
    import string
    import random
    
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def check_password_strength(password: str) -> Dict[str, Any]:
    score = 0
    feedback = []
    suggestions = []
    
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("كلمة المرور قصيرة جداً")
        suggestions.append("استخدم 8 أحرف على الأقل")
    
    if any(c.islower() for c in password):
        score += 1
    else:
        suggestions.append("أضف أحرف صغيرة")
    
    if any(c.isupper() for c in password):
        score += 1
    else:
        suggestions.append("أضف أحرف كبيرة")
    
    if any(c.isdigit() for c in password):
        score += 1
    else:
        suggestions.append("أضف أرقام")
    
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        score += 1
    else:
        suggestions.append("أضف رموز خاصة")
    
    if score < 3:
        feedback.append("كلمة مرور ضعيفة")
    elif score < 4:
        feedback.append("كلمة مرور متوسطة")
    else:
        feedback.append("كلمة مرور قوية")
    
    return {
        "score": score,
        "feedback": feedback,
        "suggestions": suggestions
    }
