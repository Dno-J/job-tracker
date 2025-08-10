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

# ⚙️ Create SQLModel engine
engine = create_engine(DATABASE_URL, echo=True)

# ---------------------------------------
# 🔁 FastAPI dependency for DB sessions
# ---------------------------------------
def get_session() -> Generator[Session, None, None]:
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

# ---------------------------------------
# 📦 Context manager for scripts or utilities
# ---------------------------------------
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
def create_db_and_tables():
    from app.models import user, job  # Ensure models are loaded
    SQLModel.metadata.create_all(engine)
