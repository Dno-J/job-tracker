import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware

from app.database import create_db_and_tables
from app.routers import auth, job, dashboard, job_api
from app.middleware.auth_middleware import AuthMiddleware
from app.utils.charts import CHART_TMP_DIR

# -------------------------------
# 📋 Logging Setup
# -------------------------------
# Configure global logging for the app
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------------
# 🚀 Application Startup Handler
# -------------------------------
# Runs once when the app starts — used to initialize DB
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting app and initializing database...")
    create_db_and_tables()  # Creates tables if they don't exist
    yield  # App runs after this

# -------------------------------
# ⚙️ FastAPI App Setup
# -------------------------------
# Instantiate FastAPI with custom lifespan handler
app = FastAPI(lifespan=lifespan)

# -------------------------------
# 📦 Middleware
# -------------------------------
# Logs every incoming request and outgoing response
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"📥 {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"📤 {response.status_code}")
        return response

# Add custom middleware to the app
app.add_middleware(LoggingMiddleware)  # Logs requests/responses
app.add_middleware(AuthMiddleware)     # Handles JWT-based auth

# -------------------------------
# 📂 Static Files & Templates
# -------------------------------
# Define paths to static assets and HTML templates
static_path = os.path.join(os.path.dirname(__file__), "app", "static")
templates_path = os.path.join(os.path.dirname(__file__), "app", "templates")

# Mount chart temp folder for dynamic chart serving (must be above /static)
app.mount("/static/tmp", StaticFiles(directory=CHART_TMP_DIR), name="tmp")
logger.info(f"✅ Chart temp mounted: {CHART_TMP_DIR}")

# Mount static files at /static (e.g. CSS, JS, images)
app.mount("/static", StaticFiles(directory=static_path), name="static")
logger.info(f"✅ Static mounted: {static_path}")

# Load Jinja2 templates for HTML rendering
templates = Jinja2Templates(directory=templates_path)
logger.info(f"✅ Templates mounted: {templates_path}")

# -------------------------------
# 🔀 Include Routers
# -------------------------------
# Modular route registration
app.include_router(auth.router)                         # /login, /register
app.include_router(job.router, prefix="/jobs")          # /jobs, /jobs/add, /jobs/edit
app.include_router(dashboard.router)                    # /dashboard
app.include_router(job_api.router, prefix="/api/jobs")  # /api/jobs/ REST API routes

# -------------------------------
# 🏠 Root & Utility Routes
# -------------------------------
# Home page — renders index.html
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Health check endpoint — useful for monitoring
@app.get("/ping")
async def ping():
    return {"message": "pong"}
