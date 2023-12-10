import pytest
from src.api_client import APIClient
from config import YANDEX_DISK_OAUTH_TOKEN


@pytest.fixture
def api_client():
    return APIClient(YANDEX_DISK_OAUTH_TOKEN)
