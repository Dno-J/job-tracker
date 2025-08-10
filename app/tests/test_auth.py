from fastapi.testclient import TestClient


def test_register_and_login(client: TestClient):
    # Register user
    register_data = {
        "username": "johndoe",
        "email": "john@example.com",
        "password": "securepass"
    }
    response = client.post("/register", data=register_data, follow_redirects=False)
    assert response.status_code == 303  # Redirect to login

    # Login user
    login_data = {
        "username": "johndoe",
        "password": "securepass"
    }
    response = client.post("/login", data=login_data, follow_redirects=False)
    assert response.status_code == 303  # Redirect to dashboard
    assert "access_token" in response.cookies


def test_protected_route_requires_auth(client: TestClient):
    # Without login, should redirect to /login
    response = client.get("/add-job", follow_redirects=False)
    assert response.status_code in (303, 307)
    assert "/login" in response.headers.get("location", "")
