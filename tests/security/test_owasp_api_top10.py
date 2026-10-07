"""OWASP API Security Top 10 style checks. crAPI is intentionally vulnerable, so some of these
SHOULD fail against it - that is the point. Write each test to assert the SECURE behaviour; a failing
test then documents a real vulnerability. Use xfail(strict=True) with a reason once you confirm one.
Only run these against your own local crAPI instance.
"""
import pytest

pytestmark = pytest.mark.security


@pytest.mark.skip(reason="TODO (you): API1 BOLA - can user A read user B's resource by changing an ID?")
def test_bola_cannot_read_other_users_data(auth_client):
    """Needs two registered users. Fetch a resource ID as user A, request it as user B."""


@pytest.mark.skip(reason="TODO (you): API2 Broken authentication - token handling, lockout, weak reset flow")
def test_repeated_failed_logins_are_limited(anon_client, registered_user):
    """Send N wrong-password logins. Does the app ever slow down or lock?"""


@pytest.mark.skip(reason="TODO (you): API3 Excessive data exposure - do responses leak fields the UI never shows?")
def test_responses_do_not_leak_sensitive_fields(auth_client):
    """Inspect dashboard and other responses for password hashes, internal IDs, tokens."""


@pytest.mark.skip(reason="TODO (you): API4 Resource consumption - missing rate limits or size limits")
def test_oversized_payload_is_rejected(anon_client):
    """Send a very large field value and check for a clean rejection."""


@pytest.mark.skip(reason="TODO (you): API6 Mass assignment - extra JSON fields accepted that should be ignored")
def test_mass_assignment_ignored(auth_client):
    """Add unexpected fields (role, credits) to an update request and see if they stick."""
