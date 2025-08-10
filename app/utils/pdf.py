import io
import os
from typing import List
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from app.models.job import Job
from app.utils.filesystem import ensure_folder

EXPORTS_DIR = "app/static/exports"

# -----------------------------
# 📄 Generate a well-formatted PDF report of jobs
# -----------------------------
def generate_pdf(jobs: List[Job], filename: str = "job_applications.pdf") -> bytes:
    ensure_folder(EXPORTS_DIR)
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=30, rightMargin=30, topMargin=30, bottomMargin=30
    )

    styles = getSampleStyleSheet()
    body_style = ParagraphStyle(name='Body', fontSize=8, leading=10)
    elements = []

    elements.append(Paragraph("Job Applications Report", styles['Title']))
    elements.append(Spacer(1, 12))

    data = [[
        Paragraph("Title", body_style),
        Paragraph("Company", body_style),
        Paragraph("Location", body_style),
        Paragraph("Status", body_style),
        Paragraph("Applied Date", body_style),
        Paragraph("Link", body_style),
        Paragraph("Notes", body_style)
    ]]

    for job in jobs:
        data.append([
            Paragraph(job.title or "-", body_style),
            Paragraph(job.company or "-", body_style),
            Paragraph(job.location or "-", body_style),
            Paragraph(job.status or "-", body_style),
            Paragraph(str(job.applied_date), body_style),
            Paragraph(job.link or "-", body_style),
            Paragraph(job.notes or "-", body_style)
        ])

    col_widths = [70, 70, 60, 60, 60, 100, 100]

    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
    ]))

    elements.append(table)
    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    # Optional: save to disk if needed
    # with open(os.path.join(EXPORTS_DIR, filename), "wb") as f:
    #     f.write(pdf)

    return pdf
