from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta
from .config import settings

security = HTTPBearer()

def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode = {**data, "exp": expire}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def require_role(required: str):
    def checker(user: dict = Depends(get_current_user)):
        if user.get("role") != required:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return checker