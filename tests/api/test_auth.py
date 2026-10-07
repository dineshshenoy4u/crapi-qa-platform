import pytest
from framework import data

pytestmark = pytest.mark.auth


def test_protected_endpoint_rejects_missing_token(anon_client):
    response = anon_client.dashboard()
    assert response.status_code in (401, 403, 404), f"Unexpected Status without token: {response.status_code} - " \
                                                    f"{response.text}"


def test_protected_endpoint_rejects_garbage_token(anon_client):
    anon_client.token = "not-a-real-token"
    response = anon_client.dashboard()
    assert response.status_code in (401, 403, 404), f"Garbage token Response - {response.status_code} - {response.text}"


def test_login_wrong_password_is_rejected(anon_client, registered_user):
    response = anon_client.login(registered_user["email"], "definitely-wrong")
    assert response.status_code in (400, 401, 403)
    assert "token" not in response.text.lower() or "invalid" in response.text.lower()


def test_signup_duplicate_email_is_rejected(anon_client, registered_user):
    """Hint: reuse registered_user['email'] with a different number and password."""
    response = anon_client.signup(registered_user["name"], registered_user["email"],
                                  data.random_phone(), data.strong_password())
    assert "already registered" in response.text.lower(), f"Got: {response.status_code} - {response.text}"
    assert response.status_code in (400, 403, 409)


@pytest.mark.xfail(strict=True, raises=AssertionError,
                   reason="User enumeration: unknown email returns a different message than wrong password")
def test_login_unknown_user(anon_client,registered_user):
    """Hint: compare the message with the wrong-password case. Do they differ? Why does that matter?"""
    response = anon_client.login(data.unique_email(), data.strong_password())
    assert "given email is not registered" in response.text.lower(), f"Got: {response.status_code} - {response.text}"
    assert response.status_code in (400, 401)
    wr_pwd = anon_client.login(registered_user["email"],data.strong_password())
    assert response.status_code == wr_pwd.status_code
    assert response.text == wr_pwd.text, "Different responses leak which emails are registered"
