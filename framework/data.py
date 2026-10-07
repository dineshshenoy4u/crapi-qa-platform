import random
import string
import uuid


def unique_email(prefix: str = "qa") -> str:
    return f"{prefix}.{uuid.uuid4().hex[:10]}@example.com"


def random_phone() -> str:
    return "9" + "".join(random.choices(string.digits, k=9))


def strong_password() -> str:
    return "Passw0rd!" + "".join(random.choices(string.ascii_letters, k=4))


def new_user() -> dict:
    return {
        "name": "QA User",
        "email": unique_email(),
        "number": random_phone(),
        "password": strong_password(),
    }
