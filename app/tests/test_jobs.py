from fastapi.testclient import TestClient
from datetime import date


def test_create_list_update_delete_job(client: TestClient):
    # Register and login
    client.post("/register", data={
        "username": "jake",
        "email": "jake@example.com",
        "password": "strongpassword"
    }, follow_redirects=True)

    login_resp = client.post("/login", data={
        "username": "jake",
        "password": "strongpassword"
    }, follow_redirects=False)

    token = login_resp.cookies.get("access_token")
    assert token is not None, "❌ Login failed — no access_token in cookies"

    client.cookies.set("access_token", token)

    # Create job
    job_payload = {
        "title": "Backend Developer Intern",
        "company": "Acme Corp",
        "status": "Interview",
        "applied_date": str(date.today()),
        "location": "Remote",
        "link": "https://acme.jobs/backend",
        "notes": "Followed up via email"
    }

    create_resp = client.post("/api/jobs/", json=job_payload)
    print("\n🔍 create_resp.status_code:", create_resp.status_code)
    print("🔍 create_resp.headers:", create_resp.headers)
    print("🔍 create_resp.text:", create_resp.text)

    assert create_resp.status_code == 200, "❌ Job creation failed — not 200"
    assert "application/json" in create_resp.headers.get("content-type", "")
    job_data = create_resp.json()
    job_id = job_data.get("id")
    assert job_id is not None, f"❌ Job ID missing: {job_data}"

    # List jobs
    list_resp = client.get("/api/jobs/")
    assert list_resp.status_code == 200
    assert any(j["id"] == job_id for j in list_resp.json())

    # Update job
    update_resp = client.put(f"/api/jobs/{job_id}", json={"status": "Offer"})
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "Offer"

    # Delete job
    delete_resp = client.delete(f"/api/jobs/{job_id}")
    assert delete_resp.status_code == 204

    # Confirm deletion
    post_delete_resp = client.get("/api/jobs/")
    assert job_id not in [j["id"] for j in post_delete_resp.json()]
