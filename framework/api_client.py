"""Thin wrapper around httpx so every test talks to the app the same way.

Endpoint paths below are based on crAPI's public docs. Confirm each one against
your running instance (Swagger / browser dev tools) and fix any that differ.
"""
import httpx

from framework.config import Settings


class ApiClient:
    def __init__(self, settings: Settings, token: str | None = None):
        self.settings = settings
        self.token = token
        self._client = httpx.Client(base_url=settings.base_url, timeout=settings.timeout)

    def _headers(self, extra: dict | None = None) -> dict:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        if extra:
            headers.update(extra)
        return headers

    def request(self, method: str, path: str, **kwargs) -> httpx.Response:
        headers = self._headers(kwargs.pop("headers", None))
        return self._client.request(method, path, headers=headers, **kwargs)

    def get(self, path: str, **kwargs) -> httpx.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> httpx.Response:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs) -> httpx.Response:
        return self.request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs) -> httpx.Response:
        return self.request("DELETE", path, **kwargs)

    def close(self) -> None:
        self._client.close()

    # --- crAPI endpoints (verify against your instance) ---

    def signup(self, name: str, email: str, number: str, password: str) -> httpx.Response:
        return self.post(
            "/identity/api/auth/signup",
            json={"name": name, "email": email, "number": number, "password": password},
        )

    def login(self, email: str, password: str) -> httpx.Response:
        return self.post("/identity/api/auth/login", json={"email": email, "password": password})

    def dashboard(self) -> httpx.Response:
        return self.get("/identity/api/v2/user/dashboard")

    def products(self, params: dict | None = None) -> httpx.Response:
        return self.get("/workshop/api/shop/products", params=params)
