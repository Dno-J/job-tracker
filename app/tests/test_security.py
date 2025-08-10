from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_protected_route_requires_login():
    resp = client.get("/api/jobs/", follow_redirects=False)
    print("\n[UNAUTHENTICATED ACCESS]")
    print("→ Redirect status:", resp.status_code)
    print("→ Redirect location:", resp.headers.get("location"))

    assert resp.status_code in (303, 307), "❌ Expected redirect for unauthenticated access"
    assert "/login" in resp.headers.get("location", ""), "❌ Should redirect to login page"

def test_tampered_cookie_blocks_access():
    client.cookies.set("access_token", "fake-token")
    resp = client.get("/api/jobs/", follow_redirects=False)
    print("\n[TAMPERED TOKEN]")
    print("→ Redirect or error status:", resp.status_code)
    print("→ Location (if redirect):", resp.headers.get("location"))

    assert resp.status_code in (303, 307, 401, 403), "❌ Tampered token should not allow access"
    # If redirect occurs, assert destination
    if resp.status_code in (303, 307):
        assert "/login" in resp.headers.get("location", ""), "❌ Should redirect to login"

def test_valid_access_token_allows_entry():
    # ⚠️ TODO: Mock a valid token flow once login and token issuance are implemented
    pass
