import csv
import io
from app.models.job import Job

# -----------------------------
# 📄 Generate downloadable CSV from job list
# -----------------------------
def generate_csv(jobs: list[Job]) -> bytes:
    """
    Converts a list of Job objects into a downloadable CSV.
    Returns UTF-8 encoded bytes.
    """
    output = io.StringIO()
    writer = csv.writer(output)

    # Header row
    writer.writerow(["Title", "Company", "Location", "Link", "Status", "Applied Date", "Notes"])

    # Job data rows
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

    return output.getvalue().encode("utf-8")
