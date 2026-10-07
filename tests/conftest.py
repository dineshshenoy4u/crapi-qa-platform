import httpx
import pytest

from framework.api_client import ApiClient
from framework.config import get_settings
from framework.data import new_user


@pytest.fixture(scope="session")
def settings():
    return get_settings()


@pytest.fixture(scope="session", autouse=True)
def require_target_app(settings):
    """Skip the whole run with a clear message if crAPI is not reachable."""
    try:
        httpx.get(settings.base_url, timeout=5)
    except httpx.HTTPError:
        pytest.skip(
            f"crAPI not reachable at {settings.base_url}. "
            "Start it with Docker first (see docs/docker-setup.md).",
            allow_module_level=False,
        )


@pytest.fixture
def anon_client(settings):
    client = ApiClient(settings)
    yield client
    client.close()


@pytest.fixture(scope="session")
def registered_user(settings):
    """Create one user for the session and return its credentials."""
    user = new_user()
    client = ApiClient(settings)
    response = client.signup(user["name"], user["email"], user["number"], user["password"])
    client.close()
    assert response.status_code in (200, 201), f"Signup failed: {response.status_code} {response.text}"
    return user


@pytest.fixture
def auth_client(settings, registered_user):
    """API client already logged in as the session user."""
    client = ApiClient(settings)
    response = client.login(registered_user["email"], registered_user["password"])
    assert response.status_code == 200, f"Login failed: {response.status_code} {response.text}"
    client.token = response.json().get("token")
    assert client.token, "Login response had no token field - check the response shape"
    yield client
    client.close()
