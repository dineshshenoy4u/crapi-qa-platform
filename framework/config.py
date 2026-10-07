import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    base_url: str
    mailhog_url: str
    timeout: float


def get_settings() -> Settings:
    return Settings(
        base_url=os.getenv("CRAPI_BASE_URL", "http://localhost:8888").rstrip("/"),
        mailhog_url=os.getenv("CRAPI_MAILHOG_URL", "http://localhost:8025").rstrip("/"),
        timeout=float(os.getenv("REQUEST_TIMEOUT_SECONDS", "15")),
    )
