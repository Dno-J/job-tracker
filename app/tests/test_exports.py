from fastapi.testclient import TestClient
from datetime import date


def test_pdf_and_csv_export(client: TestClient):
    # Setup: Register, login, authenticate
    client.post("/register", data={
        "username": "alice",
        "email": "alice@example.com",
        "password": "topsecret"
    }, follow_redirects=True)

    login = client.post("/login", data={
        "username": "alice",
        "password": "topsecret"
    }, follow_redirects=False)

    token = login.cookies.get("access_token")
    assert token is not None
    client.cookies.set("access_token", token)

    # Create job so export isn't empty
    job_payload = {
        "title": "Python Developer",
        "company": "ExampleCorp",
        "status": "Applied",
        "applied_date": str(date.today()),
        "location": "Hybrid",
        "link": "https://example.com/jobs/python-dev",
        "notes": "Applied via job portal"
    }
    client.post("/api/jobs/", json=job_payload)

    # ✅ PDF Export
    pdf_resp = client.get("/jobs/export/pdf")
    assert pdf_resp.status_code == 200
    assert pdf_resp.headers.get("content-type") == "application/pdf"
    assert "attachment; filename=job_applications.pdf" in pdf_resp.headers.get("content-disposition", "")

    # ✅ CSV Export
    csv_resp = client.get("/jobs/export/csv")
    assert csv_resp.status_code == 200
    assert "text/csv" in csv_resp.headers.get("content-type", "")
    assert "attachment; filename=job_applications.csv" in csv_resp.headers.get("content-disposition", "")
