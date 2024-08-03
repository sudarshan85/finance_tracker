import pytest
import os

@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    """Cleanup a testing directory once we are finished."""
    def remove_test_db():
        os.unlink("./test.db")
    request.addfinalizer(remove_test_db)