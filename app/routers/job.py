from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse, HTMLResponse, StreamingResponse
from sqlmodel import Session
from io import BytesIO

from app.database import get_session
from app.auth.jwt import get_current_user
from app.models.user import User
from app.models.job import Job
from app.utils.templates import templates
from app.utils.pdf import generate_pdf
from app.utils.csv import generate_csv

router = APIRouter()

# -------------------------------
# 📝 Add Job Form (GET)
# -------------------------------
@router.get("/add-job", response_class=HTMLResponse)
def add_job_form(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("add_job.html", {"request": request})

# -------------------------------
# 📝 Add Job Submit (POST)
# -------------------------------
@router.post("/add-job")
def add_job(
    request: Request,
    title: str = Form(...),
    company: str = Form(...),
    location: str = Form(None),
    status: str = Form(...),
    link: str = Form(None),
    applied_date: str = Form(...),
    notes: str = Form(None),
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Create and persist job entry
    job = Job(
        title=title,
        company=company,
        location=location,
        status=status,
        link=link,
        applied_date=applied_date,
        notes=notes,
        user_id=current_user.id
    )
    db.add(job)
    db.commit()
    return RedirectResponse(url="/dashboard", status_code=303)

# -------------------------------
# ✏️ Edit Job Form (GET)
# -------------------------------
@router.get("/edit-job/{job_id}", response_class=HTMLResponse)
def edit_job_form(
    job_id: int,
    request: Request,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    job = db.get(Job, job_id)
    if not job or job.user_id != current_user.id:
        return RedirectResponse(url="/dashboard", status_code=303)
    return templates.TemplateResponse("edit_job.html", {"request": request, "job": job})

# -------------------------------
# 📄 Export Jobs as PDF
# -------------------------------
@router.get("/export/pdf")
def export_pdf(
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    jobs = db.query(Job).filter(Job.user_id == current_user.id).all()
    pdf_bytes = generate_pdf(jobs)
    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=job_applications.pdf"},
    )

# -------------------------------
# 📄 Export Jobs as CSV
# -------------------------------
@router.get("/export/csv")
def export_csv(
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    jobs = db.query(Job).filter(Job.user_id == current_user.id).all()
    csv_bytes = generate_csv(jobs)
    return StreamingResponse(
        BytesIO(csv_bytes),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=job_applications.csv"},
    )
