import pytest

from app.main import initiateFlask


@pytest.fixture(autouse=True)
def run_before_all_tests(tmpdir):
    with initiateFlask().app_context():
        yield
