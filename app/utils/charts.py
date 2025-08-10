import os
from collections import Counter
from datetime import datetime, date
import matplotlib
matplotlib.use('Agg')  # ✅ Non-interactive backend for server environments
import matplotlib.pyplot as plt

from app.models.job import Job
from app.utils.filesystem import ensure_folder

# -----------------------------
# 📁 Ensure charts output folder exists
# -----------------------------
CHARTS_DIR = "app/static/charts"
ensure_folder(CHARTS_DIR)

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

    path = os.path.join(CHARTS_DIR, "job_status_chart.png")
    ensure_folder(os.path.dirname(path))
    plt.savefig(path)
    plt.close()

    return "/static/charts/job_status_chart.png"

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

    path = os.path.join(CHARTS_DIR, "job_applications_over_time.png")
    ensure_folder(os.path.dirname(path))
    plt.savefig(path)
    plt.close()

    return "/static/charts/job_applications_over_time.png"
