from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select
from collections import Counter

from app.database import get_session
from app.auth.jwt import get_current_user
from app.models.user import User
from app.models.job import Job
from app.utils.templates import templates
from app.utils.charts import generate_status_chart, generate_time_chart

router = APIRouter()

# -------------------------------
# 📊 Dashboard View
# -------------------------------
@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(
    request: Request,
    status: str = Query(default=None, alias="status"),
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Render the dashboard for the authenticated user, showing their job applications
    and charts summarizing job statuses over time.
    """
    # Fetch all jobs for the user
    all_jobs = db.exec(select(Job).where(Job.user_id == current_user.id)).all()

    # Filter jobs by status if provided
    if status and status.lower() != "all":
        filtered_jobs = [job for job in all_jobs if job.status.lower() == status.lower()]
    else:
        filtered_jobs = all_jobs

    # Count jobs by status
    statuses = ['Applied', 'Interviewing', 'Offer Received', 'Rejected', 'Saved']
    counter = Counter(job.status for job in all_jobs)
    summary = {"Total": len(all_jobs)}
    for s in statuses:
        summary[s] = counter.get(s, 0)

    # Generate charts (saved as PNGs in static folder)
    status_chart = generate_status_chart(all_jobs)
    time_chart = generate_time_chart(all_jobs)

    # Render dashboard template
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": current_user,
            "jobs": filtered_jobs,
            "summary": summary,
            "status_chart": status_chart,
            "time_chart": time_chart,
            "status_filter": status,
        },
    )
