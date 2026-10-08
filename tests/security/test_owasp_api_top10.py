"""OWASP API Security Top 10 style checks. crAPI is intentionally vulnerable, so some of these
SHOULD fail against it - that is the point. Write each test to assert the SECURE behaviour; a failing
test then documents a real vulnerability. Use xfail(strict=True) with a reason once you confirm one.
Only run these against your own local crAPI instance.
"""
import pytest

from framework import data

pytestmark = pytest.mark.security


def test_second_client_is_a_different_user(auth_client,second_auth_client):
    user_a = auth_client.dashboard()
    user_b = second_auth_client.dashboard()
    assert user_a.status_code == 200
    assert user_b.status_code == 200
    assert auth_client.token != second_auth_client.token
    assert user_a.json()["email"] != user_b.json()["email"]

@pytest.mark.xfail(strict=True,raises=AssertionError,
                   reason="BOLA: any logged-in user can read another user's order (PII + Payment details)")
def test_bola_cannot_read_other_users_data(auth_client,second_auth_client):
    """Needs two registered users. Fetch a resource ID as user A, request it as user B."""
    created = auth_client.post("/workshop/api/shop/orders", json={"product_id": 2, "quantity": 1})
    order_id = created.json()["id"]
    response_a = auth_client.get(f"/workshop/api/shop/orders/{order_id}")
    assert response_a.status_code == 200
    response_b = second_auth_client.get(f"/workshop/api/shop/orders/{order_id}")
    assert response_b.status_code in (400, 401, 403, 404), f"Second user was able to access the order id {order_id}, which is First User order"


@pytest.mark.parametrize("extra",[{"status":"return pending"}, {"credit":1000}])
def test_mass_assignment_ignored(auth_client, extra):
    credit_before = auth_client.dashboard().json()["available_credit"]
    body = {"product_id": 2, "quantity": 1, **extra}
    created = auth_client.post("/workshop/api/shop/orders", json=body)
    assert created.status_code == 200, f"Got {created.status_code}: {created.text}"
    order_id = created.json()["id"]

    order = auth_client.get(f"/workshop/api/shop/orders/{order_id}")
    assert order.json()["order"]["status"] == "delivered", f"Extra Field {extra} changed the status"

    credit_after = auth_client.dashboard().json()["available_credit"]
    assert credit_after == credit_before - 10, f"Extra field {extra} changed the credit"

@pytest.mark.skip(reason="TODO (you): API2 Broken authentication - token handling, lockout, weak reset flow")
def test_repeated_failed_logins_are_limited(anon_client, registered_user):
    """Send N wrong-password logins. Does the app ever slow down or lock?"""

@pytest.mark.xfail(strict=True,raises=AssertionError,reason="Excessive Data Exposure: community posts author email and vehicleid to any user")
def test_responses_do_not_leak_sensitive_fields(auth_client):
    """Inspect dashboard and other responses for password hashes, internal IDs, tokens."""
    response = auth_client.get("/community/api/v2/community/posts/recent",params={"limit": 30, "offset": 0})
    assert response.status_code == 200
    assert "nickname" in response.text, f"Nickname of the Author not observed"
    assert "email" not in response.text, f"Author email is exposed in community posts"
    assert "vehicleid" not in response.text, f"Author vehicle id is exposed in community posts"


def test_oversized_payload_is_rejected(anon_client):
    """Send a very large field value and check for a clean rejection."""
    user = data.new_user()
    user["name"] = "a"*1000000
    response = anon_client.signup(user["name"], user["email"], user["number"],user["password"])
    assert response.status_code in (400, 413), f"Got following error - {response.status_code} "
    assert "token" not in response.text.lower()

