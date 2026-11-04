def test_contexts_are_isolated(two_contexts):
    context1, context2 = two_contexts

    context1.add_cookies([
    {
        "name": "session_id",
        "value": "user1",
        "url": "https://example.com"
    }
])

    cookie1 = context1.cookies()
    cookie2 = context2.cookies()

    assert any(cookie["name"] == "session_id" for cookie in cookie1)
    assert not any(cookie["name"] == "session_id" for cookie in cookie2)

