from datetime import date
from pydantic import BaseModel, ConfigDict, HttpUrl
from typing import Optional

# ---------------------------------
# 📄 Base job schema (shared fields)
# ---------------------------------
class JobBase(BaseModel):
    """
    Common fields shared across job creation, update, and read schemas.
    """

    title: str
    # Job title (e.g., "Backend Developer Intern").

    company: str
    # Company name.

    location: Optional[str] = None
    # Job location. Optional.

    link: Optional[HttpUrl] = None
    # Validated URL to job posting. Optional.

    status: Optional[str] = "Applied"
    # Application status. Defaults to "Applied".

    notes: Optional[str] = None
    # Freeform notes. Optional.

    model_config = ConfigDict(from_attributes=True)
    # Enables compatibility with ORM-style models.

# ---------------------------------
# ➕ Schema for creating a job
# ---------------------------------
class JobCreate(JobBase):
    """
    Schema used when creating a new job entry.
    """
    applied_date: date
    # Date the user applied for the job.

# ---------------------------------
# ✏️ Schema for updating a job
# ---------------------------------
class JobUpdate(BaseModel):
    """
    Schema used when updating an existing job entry.
    All fields are optional to allow partial updates.
    """

    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    link: Optional[HttpUrl] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    applied_date: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)

# ---------------------------------
# 🔁 Schema used when reading jobs
# ---------------------------------
class JobRead(JobBase):
    """
    Schema used when returning job data from the API.
    Includes database-generated fields.
    """

    id: int
    # Unique job ID.

    applied_date: date
    # Date the job was applied to.

    user_id: int
    # ID of the user who created the job.

    model_config = ConfigDict(from_attributes=True)
