"""Schema/contract checks with pydantic: assert the response SHAPE, not just a status code."""
import pytest
from pydantic import BaseModel


class LoginResponse(BaseModel):
    token: str
    type: str
    message: str
    mfaRequired: bool

class Product(BaseModel):
    id: int
    name: str
    price: str
    image_url: str

class ProductResponse(BaseModel):
    products: list[Product]
    credit: float
    count: int


def test_login_response_matches_schema(anon_client, registered_user):
    response = anon_client.login(registered_user["email"], registered_user["password"])
    assert response.status_code == 200
    LoginResponse.model_validate(response.json())


def test_products_list_matches_schema(auth_client):
    """Hint: print the JSON once, build the model from it, then validate all items in the list."""
    response = auth_client.products(params={"limit":30})
    assert response.status_code == 200
    ProductResponse.model_validate(response.json())
