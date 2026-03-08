from services.middleware.request_context import get_login_context


def test_request_context(rf):

    request = rf.get("/", HTTP_USER_AGENT="pytest")

    ctx = get_login_context(request)

    assert "ip" in ctx