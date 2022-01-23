import pytest

from app.main import initiateFlask

context = dict(
    app=initiateFlask(),
)


@pytest.fixture(autouse=True)
def run_before_all_tests():
    with context['app'].app_context():
        yield


@pytest.fixture(scope="function", autouse=True)
def client():
    with context['app'].test_client() as client:
        return client
