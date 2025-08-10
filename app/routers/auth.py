import os
import logging
from fastapi import APIRouter, Request, Form, status, Depends, Cookie, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlmodel import Session
from jose import JWTError, jwt

from app.database import get_session
from app.auth.password import hash_password, verify_password
from app.auth.jwt import create_access_token
from app.models.user import User
from app.utils.templates import templates

router = APIRouter()

# -------------------------------
# 🔐 JWT Config (temporary)
# -------------------------------
# ⛔ Hardcoded secret — replace with config import in production
from config import settings
SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM

# -------------------------------
# 🔍 Dependency to get current user from JWT cookie
# -------------------------------
def get_current_user(
    access_token: str = Cookie(default=None),
    db: Session = Depends(get_session)
) -> User:
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing access token")

    try:
        # Decode JWT and extract username
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing username")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    # Query user from DB
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user

# -------------------------------
# 📝 Register Form (GET)
# -------------------------------
@router.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "error": None})

# -------------------------------
# 📝 Register Submit (POST)
# -------------------------------
@router.post("/register")
def register_user(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_session)
):
    # Clean input
    username = username.strip()
    email = email.strip()

    # Check for existing user
    existing_user = db.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()

    if existing_user:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "User already exists. Try a different username or email."
        })

    # Hash password and create user
    hashed_pw = hash_password(password)
    new_user = User(username=username, email=email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Redirect to login
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

# -------------------------------
# 🔐 Login Form (GET)
# -------------------------------
@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# -------------------------------
# 🔐 Login Submit (POST)
# -------------------------------
@router.post("/login")
def login_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_session)
):
    username = username.strip()
    user = db.query(User).filter(User.username == username).first()

    # Validate credentials
    if not user or not verify_password(password, user.hashed_password):
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JSONResponse({"error": "Invalid username or password"}, status_code=400)
        else:
            return templates.TemplateResponse("login.html", {
                "request": request,
                "error": "Invalid username or password"
            })

    # Create JWT and set cookie
    access_token = create_access_token({"sub": user.username})
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # ✅ Set True in production with HTTPS
        samesite="lax"
    )
    return response

# -------------------------------
# 🚪 Logout Route
# -------------------------------
@router.get("/logout")
def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response
