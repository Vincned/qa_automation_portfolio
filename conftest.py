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


@pytest.fixture(scope="function")
def created_user(api_client, request):
    user_id = None
    
    def cleanup():
        if user_id is not None:
            api_client.delete(f"/users/{user_id}")
        
    request.addfinalizer(cleanup)
    
    payload = {
    "name": "Test User",
    "username": "test_user",
    "email": "test@example.com"
}
    
    response = api_client.post("/users", payload)
    response.raise_for_status()
    user_json = response.json()
    user_id = user_json["id"]

    yield user_id


@pytest.fixture
def created_post(api_client, request, created_user):
    post_id = None

    def cleanup():
        if post_id is not None:
            api_client.delete(f"/posts/{post_id}")
    
    request.addfinalizer(cleanup)

    payload = {
        "userId": created_user,
        "title": "Test Post",
        "body": "Test post body",
    }

    response = api_client.post("/posts", payload)
    response.raise_for_status()
    post_json = response.json()
    id_of_the_post = post_json["id"]

    yield id_of_the_post
