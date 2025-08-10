import os
from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
from typing import Generator
from contextlib import contextmanager

# 📦 Load environment variables from .env file
load_dotenv()

# 🔗 Get the database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# 🛑 Fail fast if DATABASE_URL is missing
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set in .env file")

# ⚙️ Create SQLModel engine with echo enabled for SQL logging
engine = create_engine(DATABASE_URL, echo=True)

# ---------------------------------------
# 🔁 FastAPI dependency for DB sessions
# ---------------------------------------
# Used in route functions via Depends(get_session)
def get_session() -> Generator[Session, None, None]:
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

# ---------------------------------------
# 📦 Context manager for scripts or utilities
# ---------------------------------------
# Allows usage like: with get_session_context() as session:
@contextmanager
def get_session_context():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

# ---------------------------------------
# 🏗️ Create all tables on app startup
# ---------------------------------------
# Imports models to register them with SQLModel metadata
def create_db_and_tables():
    from app.models import user, job  # Ensure models are loaded
    SQLModel.metadata.create_all(engine)
