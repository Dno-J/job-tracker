import csv
import io
import os
from app.models.job import Job
from app.utils.filesystem import ensure_folder

EXPORTS_DIR = "app/static/exports"

# -----------------------------
# 📄 Generate downloadable CSV from job list
# -----------------------------
def generate_csv(jobs: list[Job], filename: str = "job_applications.csv") -> bytes:
    ensure_folder(EXPORTS_DIR)
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["Title", "Company", "Location", "Link", "Status", "Applied Date", "Notes"])

    for job in jobs:
        writer.writerow([
            job.title,
            job.company,
            job.location or "",
            job.link or "",
            job.status,
            job.applied_date,
            job.notes or ""
        ])

    # Optional: save to disk if needed
    # with open(os.path.join(EXPORTS_DIR, filename), "wb") as f:
    #     f.write(output.getvalue().encode("utf-8"))

    return output.getvalue().encode("utf-8")
