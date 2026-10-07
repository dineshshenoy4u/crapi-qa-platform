import pytest

pytestmark = pytest.mark.smoke


def test_web_root_responds(anon_client):
    response = anon_client.get("/")
    assert response.status_code == 200


def test_login_returns_token(auth_client):
    assert auth_client.token


def test_dashboard_returns_user_data(auth_client, registered_user):
    response = auth_client.dashboard()
    assert response.status_code == 200
    body = response.json()
    assert body.get("email") == registered_user["email"]
