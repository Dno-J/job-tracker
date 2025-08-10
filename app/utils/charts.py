import os
from collections import Counter
from datetime import datetime, date
import matplotlib
matplotlib.use('Agg')  # ✅ Non-interactive backend for server environments
import matplotlib.pyplot as plt

from app.models.job import Job
from app.utils.filesystem import ensure_folder

# -----------------------------
# 📁 Chart output path resolver
# -----------------------------
def get_chart_path(filename: str) -> tuple[str, str]:
    """
    Returns (absolute_path, public_url) based on environment.
    In production, saves to /tmp; locally, saves to static folder.
    """
    if os.getenv("ENV") == "production":
        return f"/tmp/{filename}", f"/tmp/{filename}"
    else:
        charts_dir = "app/static/charts"
        ensure_folder(charts_dir)
        return os.path.join(charts_dir, filename), f"/static/charts/{filename}"

# -----------------------------
# 📊 Generate bar chart of job statuses
# -----------------------------
def generate_status_chart(jobs: list[Job]) -> str | None:
    counts = Counter(job.status for job in jobs if job.status)
    if not counts:
        return None

    statuses = list(counts.keys())
    values = list(counts.values())

    plt.figure(figsize=(6, 4))
    plt.bar(statuses, values, color="#2563EB")
    plt.title("Job Status Overview")
    plt.ylabel("Number of Applications")
    plt.tight_layout()

    path, url = get_chart_path("job_status_chart.png")
    plt.savefig(path)
    plt.close()

    return url

# -----------------------------
# 📈 Generate line chart of applications over time
# -----------------------------
def generate_time_chart(jobs: list[Job]) -> str | None:
    valid_dates = [job.applied_date for job in jobs if isinstance(job.applied_date, (date, datetime))]
    if not valid_dates:
        return None

    date_counts = Counter(valid_dates)
    dates = sorted(date_counts.keys())
    values = [date_counts[dt] for dt in dates]

    plt.figure(figsize=(7, 4))
    plt.plot(dates, values, marker='o', color="#059669")
    plt.title("Applications Over Time")
    plt.xlabel("Date")
    plt.ylabel("Applications")
    plt.xticks(rotation=45)
    plt.tight_layout()

    path, url = get_chart_path("job_applications_over_time.png")
    plt.savefig(path)
    plt.close()

    return url
