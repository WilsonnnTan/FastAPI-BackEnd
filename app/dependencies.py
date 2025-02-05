from fastapi import Depends, HTTPException
from app.auth.jwt import verify_token
from app.models.user import User
from app.database import SessionLocal

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = User.get_user_by_id(payload.get("sub"))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
