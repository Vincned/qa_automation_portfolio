import pytest

def test_created_post(created_post):
    post_id = created_post
    #int or not
    assert isinstance(created_post, int)
    #more than 0
    assert post_id > 0

def test_get_post(api_client):
    response = api_client.get("/posts/1")
    #status code check
    assert response.status_code == 200
    #json
    post_json = response.json()
    #check id from the json
    assert post_json["id"] == 1
    #title
    assert isinstance(post_json["title"], str)
    assert isinstance(post_json["body"], str)

def test_created_comment(created_comment):
    comment_id = created_comment

    assert isinstance(comment_id, int)
    assert comment_id > 0
