from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Request, HTTPException, Depends
from jose import JWTError, jwt
from sqlmodel import Session, select
from starlette.status import HTTP_401_UNAUTHORIZED

from app.models.user import User
from app.database import get_session
from config import settings

# -----------------------------
# 🔐 Create a JWT access token
# -----------------------------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Encodes a JWT token with expiration.
    `data` should include a 'sub' field (e.g., username).
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# -----------------------------
# ✅ Verify a JWT token
# -----------------------------
def verify_access_token(token: str) -> Optional[dict]:
    """
    Decodes and validates a JWT token.
    Returns payload if valid, None if invalid.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

# -----------------------------------------------------
# 👤 Get current user from JWT stored in cookie
# -----------------------------------------------------
async def get_current_user(
    request: Request,
    session: Session = Depends(get_session)
):
    """
    Extracts JWT from cookie, verifies it, and returns the user.
    Raises 401 if token is missing, invalid, or user not found.
    """
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token")

    username: str = payload.get("sub")
    if not username:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="User not found")

    return user
