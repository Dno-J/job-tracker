from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
from pydantic import ConfigDict

class User(SQLModel, table=True):
    """
    Represents a registered user in the job tracker system.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    # Primary key — unique identifier for each user.

    username: str = Field(index=True, unique=True)
    # Unique username chosen by the user.

    email: str = Field(index=True, unique=True)
    # Unique email address used for login and communication.

    hashed_password: str
    # Securely hashed password stored in the database.

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    # Timestamp of user registration. Defaults to current UTC time.

    model_config = ConfigDict(from_attributes=True)
    # Enables ORM-style access and compatibility with Pydantic responses.
