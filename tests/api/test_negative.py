import pytest
from framework import data

pytestmark = pytest.mark.negative


@pytest.mark.parametrize("blank_field", ["name", "email", "number", "password"])
def test_signup_blank_required_fields(anon_client, blank_field):
    """Use @pytest.mark.parametrize over name / email / number / password."""
    user = data.new_user()
    user[blank_field] = ""
    response = anon_client.signup(user["name"], user["email"], user["number"],user["password"])
    assert response.status_code == 400, f"Got {response.status_code}: {response.text}"


@pytest.mark.parametrize("missing_field", ["name", "email", "number", "password"])
def test_signup_missing_required_fields(anon_client, missing_field):
    """Use @pytest.mark.parametrize over name / email / number / password."""
    user = data.new_user()
    del user[missing_field]
    response = anon_client.post("/identity/api/auth/signup", json=user)
    assert response.status_code == 400, f"Got {response.status_code}: {response.text}"
    assert "token" not in response.text.lower()


@pytest.mark.parametrize("field, bad_value",[("email","namegmail.com"), ("email","a@@b"),
                                             ("email","namegmailcom"), ("email", " "),
                                             ("email","@gmailcom"), ("email","name@"),
                                             ("email", "a"*300+"@gmail.com"), ("email", None)])
def test_signup_email_invalid_values(anon_client, field, bad_value):
    """Try: no @, empty string, very long string, number instead of string, null."""
    user = data.new_user()
    user[field] = bad_value
    response = anon_client.post("/identity/api/auth/signup", json=user)
    assert response.status_code == 400, f"Status code observed {response.status_code} - {response.text} "
    assert "token" not in response.text.lower()


XFAIL_NUMBER = pytest.mark.xfail(
    strict=True,
    reason="Weak validation: phone number accepts letters, symbols and short values",
)
@pytest.mark.parametrize("field, bad_value", [
    pytest.param("number", "abcdefghi", marks=XFAIL_NUMBER),
    pytest.param("number", "1234,1234", marks=XFAIL_NUMBER),
    pytest.param("number", "123", marks=XFAIL_NUMBER),
    pytest.param("number", "@!@#$", marks=XFAIL_NUMBER),
    ("number", " "),
    ("number", "1" * 300),
    ("number", None),
])
def test_signup_number_invalid_values(anon_client, field, bad_value):
    """Try: no @, empty string, very long string, number instead of string, null."""
    user = data.new_user()
    user[field] = bad_value
    response = anon_client.post("/identity/api/auth/signup", json=user)
    assert response.status_code == 400, f"Status code observed {response.status_code} - {response.text} "
    assert "token" not in response.text.lower()


@pytest.mark.parametrize("bad_value",["abc"," ","name@","a2!"*150, None])
def test_signup_password_invalid_values(anon_client, bad_value):
    """Try: no @, empty string, very long string, number instead of string, null."""
    user = data.new_user()
    user["password"] = bad_value
    response = anon_client.post("/identity/api/auth/signup", json=user)
    assert response.status_code == 400, f"Status code observed {response.status_code} - {response.text} "
    assert "token" not in response.text.lower()


@pytest.mark.xfail(strict=True, reason= "Weak password policy: common passwords (123456, password, ...) are accepted")
@pytest.mark.parametrize("weakpwd", ["abcdef", "123456","password","qwerty123"])
def test_signup_password_weak_values(anon_client, weakpwd):
    """Try: no @, empty string, very long string, number instead of string, null."""
    user = data.new_user()
    user["password"] = weakpwd
    response = anon_client.post("/identity/api/auth/signup", json=user)
    assert response.status_code == 400, f"Status code observed {response.status_code} - {response.text} "
    assert "token" not in response.text.lower()


@pytest.mark.parametrize("name_size, expected_status", [(2,400), (3,200), (100,200), (101,400)])
def test_signup_name_boundary_values(anon_client,name_size,expected_status):
    """Find the real limits by probing, then assert them."""
    user = data.new_user()
    user["name"] = ("Aa1!" * 30)[:name_size]
    response = anon_client.post("/identity/api/auth/signup", json=user)
    assert response.status_code == expected_status, f"Min or Max name characters given. Name Size: {name_size} \n Response code : {response.status_code} - {response.text}"
    assert "token" not in response.text.lower()

@pytest.mark.parametrize("pwd_size, expected_status", [(5,400), (6,200), (100,200), (101,400)])
def test_signup_pwd_boundary_values(anon_client,pwd_size,expected_status):
    """Find the real limits by probing, then assert them."""
    user = data.new_user()
    user["password"] = ("Aa1!" * 30)[:pwd_size]
    response = anon_client.post("/identity/api/auth/signup", json=user)
    assert response.status_code == expected_status, f"Min or Max password characters given. PWD Size = {pwd_size} \n Response code : {response.status_code} - {response.text}"
    assert "token" not in response.text.lower()


@pytest.mark.parametrize("params", [
    {"limit": -1},
    {"limit": 0},
    {"limit": "abc"},
    {"limit": 999999},
    {"offset": -1},
    {"offset": "abc"},
])
def test_products_bad_params(auth_client,params):
    """Check the app returns a clean 4xx and not a 500 or a stack trace."""
    response = auth_client.products(params=params)
    assert response.status_code < 500, f"{params}: got {response.status_code}"
    assert "products" in response.json()


def test_products_params_control(auth_client):
    response = auth_client.products(params={"limit": 1})
    assert response.json()["count"] == 1