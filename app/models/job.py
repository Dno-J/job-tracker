from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date
from pydantic import ConfigDict

class Job(SQLModel, table=True):
    """
    Represents a job or internship application submitted by a user.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    # Primary key — unique identifier for each job entry.

    title: str
    # Job title (e.g., "Backend Developer Intern").

    company: str
    # Company name offering the job.

    location: Optional[str] = None
    # Job location (e.g., "Remote", "Bangalore"). Optional.

    link: Optional[str] = None
    # URL to job posting or application form. Optional.

    status: str = Field(default="Applied")
    # Application status. Options: Applied, Interviewing, Offer Received, Rejected, Saved.

    applied_date: date = Field(default_factory=date.today)
    # Date the user applied. Defaults to today.

    notes: Optional[str] = None
    # Freeform notes (e.g., follow-up reminders, recruiter contact). Optional.

    user_id: int = Field(foreign_key="user.id")
    # Foreign key linking job to the user who created it.

    model_config = ConfigDict(from_attributes=True)
    # Enables ORM-style access and compatibility with Pydantic responses.
