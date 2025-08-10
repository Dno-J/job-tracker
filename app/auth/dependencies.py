import os
from fastapi import Depends, HTTPException, status, Request
from jose import JWTError, jwt
from sqlmodel import Session, select

from app.models.user import User
from app.database import get_session

# ----------------------------
# 🔐 JWT Configuration
# ----------------------------
# Load secret key from environment (fallback for dev)
SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")  # ⛔ Replace with config import in production
ALGORITHM = "HS256"

# ---------------------------------------------------
# 🔍 Extract token from Authorization header or cookie
# ---------------------------------------------------
def get_token_from_request(request: Request) -> str | None:
    """
    Attempts to extract a JWT token from either:
    1. Authorization header (Bearer scheme)
    2. Cookie named 'access_token'
    """
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header[len("Bearer "):]

    return request.cookies.get("access_token")

# -----------------------------------------------------
# 👤 Get current authenticated user (used in route deps)
# -----------------------------------------------------
async def get_current_user(
    request: Request,
    session: Session = Depends(get_session)
) -> User:
    """
    Validates the JWT token and returns the associated user.
    Raises 401 if token is missing, invalid, or user not found.
    """
    token = get_token_from_request(request)

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not token:
        raise credentials_exception

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise credentials_exception

    return user
