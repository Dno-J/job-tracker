import os
import uuid
import time
import tempfile
from collections import Counter
from datetime import datetime, date
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from app.models.job import Job

# -----------------------------
# 📁 Safe temp folder for charts
# -----------------------------
# Uses system temp directory and isolates chart files
CHART_TMP_DIR = os.path.join(tempfile.gettempdir(), "job_tracker_charts")
os.makedirs(CHART_TMP_DIR, exist_ok=True)

# -----------------------------
# 🧹 Cleanup old charts in temp folder
# -----------------------------
def cleanup_tmp_folder(max_age_seconds=3600):
    now = time.time()
    for fname in os.listdir(CHART_TMP_DIR):
        path = os.path.join(CHART_TMP_DIR, fname)
        if os.path.isfile(path) and now - os.path.getmtime(path) > max_age_seconds:
            os.remove(path)

# -----------------------------
# 📁 Chart output path resolver
# -----------------------------
def get_chart_path(filename: str) -> tuple[str, str]:
    return os.path.join(CHART_TMP_DIR, filename), f"/static/tmp/{filename}"

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

    filename = f"job_status_chart_{uuid.uuid4().hex}.png"
    path, url = get_chart_path(filename)
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

    filename = f"job_applications_over_time_{uuid.uuid4().hex}.png"
    path, url = get_chart_path(filename)
    plt.savefig(path)
    plt.close()

    return url
