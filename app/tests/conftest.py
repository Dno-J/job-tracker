import pytest
import warnings
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session, create_engine

from main import app
from app.database import get_session, engine as base_engine
from app.models import job, user  # Ensure models are registered

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Create tables once for test run
SQLModel.metadata.create_all(base_engine)


@pytest.fixture()
def db() -> Generator[Session, None, None]:
    connection = base_engine.connect()
    txn = connection.begin()
    TestingSessionLocal = sessionmaker(
        bind=connection,
        class_=Session,
        expire_on_commit=False
    )
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        txn.rollback()
        connection.close()


@pytest.fixture()
def client(db: Session) -> Generator[TestClient, None, None]:
    def override_get_session():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
