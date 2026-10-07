import pytest

@pytest.fixture(scope="session")
def shared():
    print("\n[shared built]")
    return "one for all"

@pytest.fixture
def per_test(shared):
    print("[per_test built]")
    return "fresh each time"

def test_one(per_test):
    assert per_test

def test_two(per_test):
    assert per_test

def test_three(per_test):
    assert per_test