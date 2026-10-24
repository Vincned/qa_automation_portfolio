import os
import pytest
from client.api_client import APIClient
from dotenv import load_dotenv

#load configurations from .env
load_dotenv()

#creating APIClient with getting address
@pytest.fixture
def api_client():
    #get configurations
    base_url = os.getenv("API_BASE_URL")
    #if not address - get error
    if not base_url:
        raise RuntimeError("API_BASE_URL is not configured")

    return APIClient(base_url=base_url)
