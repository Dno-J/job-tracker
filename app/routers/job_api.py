from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from app.database import get_session
from app.auth.jwt import get_current_user
from app.models.user import User
from app.models.job import Job
from app.schemas.job_schemas import JobCreate, JobRead, JobUpdate

router = APIRouter()

# -------------------------------
# 🆕 Create Job (API)
# -------------------------------
@router.post("/", response_model=JobRead)
def create_job(
    job: JobCreate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    job_data = job.dict()
    if job_data.get("link"):
        job_data["link"] = str(job_data["link"])

    db_job = Job(**job_data, user_id=current_user.id)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

# -------------------------------
# 📥 Get All Jobs (API)
# -------------------------------
@router.get("/", response_model=List[JobRead])
def get_jobs(
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    jobs = db.exec(select(Job).where(Job.user_id == current_user.id)).all()
    return jobs

# -------------------------------
# ✏️ Update Job (API)
# -------------------------------
@router.put("/{job_id}", response_model=JobRead)
def update_job(
    job_id: int,
    updated_job: JobUpdate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    job = db.get(Job, job_id)
    if not job or job.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Job not found or unauthorized")

    update_data = updated_job.dict(exclude_unset=True)
    if "link" in update_data:
        update_data["link"] = str(update_data["link"])

    for key, value in update_data.items():
        setattr(job, key, value)

    db.add(job)
    db.commit()
    db.refresh(job)
    return job

# -------------------------------
# ❌ Delete Job (API)
# -------------------------------
@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(
    job_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    job = db.get(Job, job_id)
    if not job or job.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Job not found or unauthorized")

    db.delete(job)
    db.commit()
    return
