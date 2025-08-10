import pytest
from fastapi.testclient import TestClient

from main import app

# IMPORTANT: Adjust the import below to your actual auth dependency location.
# Common locations: app.dependencies, app.auth, app.core.auth
try:
    from app.dependencies import get_current_user  # <-- change this if needed
except Exception:  # pragma: no cover
    try:
        from app.auth import get_current_user  # fallback guess
    except Exception:
        get_current_user = None


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def auth_bypass():
    """
    Override authentication so CRUD tests run as an authenticated user.
    Adjust the returned user shape to match your code if you access attributes.
    """
    if get_current_user is None:
        pytest.skip("get_current_user not found. Update the import path in this test file.")

    def _fake_user():
        # Return whatever your endpoints expect for the current user.
        # dict or object with id/email is typical.
        return {"id": "test-user", "email": "test@example.com", "is_active": True}

    app.dependency_overrides[get_current_user] = _fake_user
    yield
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture
def job_payload():
    """
    Minimal valid payload. If your JobCreate requires different fields,
    update this dict to match your Pydantic model.
    """
    return {
        "title": "Backend Engineer",
        "company": "Coreline Solutions",
        "description": "Work on APIs and testing excellence.",
        "location": "Remote",
        "status": "applied",  # adjust/remove if not in your schema
    }


def create_job(client: TestClient, payload: dict) -> dict:
    resp = client.post("/api/jobs/", json=payload)
    assert resp.status_code in (200, 201), f"Expected create 200/201, got {resp.status_code}: {resp.text}"
    data = resp.json()
    assert "id" in data, f"Create response must include id. Got: {data}"
    return data


def test_create_job_success(client: TestClient, job_payload: dict):
    created = create_job(client, job_payload)
    # Soft assertions to avoid tight coupling to full schema
    assert created["title"] == job_payload["title"]
    assert created["company"] == job_payload["company"]


def test_list_jobs_includes_created(client: TestClient, job_payload: dict):
    created = create_job(client, job_payload)
    resp = client.get("/api/jobs/")
    assert resp.status_code == 200
    items = resp.json()
    # Accept both list or paginated shapes
    if isinstance(items, dict) and "items" in items:
        items = items["items"]
    ids = {item.get("id") for item in items}
    assert created["id"] in ids, "Created job must appear in listing"


def test_get_job_by_id(client: TestClient, job_payload: dict):
    created = create_job(client, job_payload)
    resp = client.get(f"/api/jobs/{created['id']}")
    assert resp.status_code == 200
    fetched = resp.json()
    assert fetched["id"] == created["id"]
    assert fetched["title"] == job_payload["title"]


def test_update_job_success(client: TestClient, job_payload: dict):
    created = create_job(client, job_payload)
    update_payload = {**job_payload, "title": "Senior Backend Engineer"}
    resp = client.put(f"/api/jobs/{created['id']}", json=update_payload)
    # Some APIs return 200; some 204 with no content. Support both.
    assert resp.status_code in (200, 204), f"Expected update 200/204, got {resp.status_code}"
    if resp.status_code == 200:
        updated = resp.json()
        assert updated["id"] == created["id"]
        assert updated["title"] == "Senior Backend Engineer"
    else:
        # If 204, fetch to verify
        get_resp = client.get(f"/api/jobs/{created['id']}")
        assert get_resp.status_code == 200
        assert get_resp.json()["title"] == "Senior Backend Engineer"


def test_delete_job_success(client: TestClient, job_payload: dict):
    created = create_job(client, job_payload)
    resp = client.delete(f"/api/jobs/{created['id']}")
    # Common patterns: 200 with body, 204 no content
    assert resp.status_code in (200, 204)
    # Verify it’s gone
    get_resp = client.get(f"/api/jobs/{created['id']}")
    assert get_resp.status_code in (404, 410), "Deleted job should not be retrievable"


def test_get_nonexistent_job_returns_404(client: TestClient):
    resp = client.get("/api/jobs/999999")
    assert resp.status_code == 404


def test_update_nonexistent_job_returns_404(client: TestClient, job_payload: dict):
    resp = client.put("/api/jobs/999999", json=job_payload)
    assert resp.status_code == 404


def test_delete_nonexistent_job_returns_404(client: TestClient):
    resp = client.delete("/api/jobs/999999")
    assert resp.status_code == 404
