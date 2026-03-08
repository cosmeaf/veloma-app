# tests/security/test_session_validation.py

from authentication.middleware.session_validation import SessionValidationMiddleware


def test_session_validation_middleware(rf):

    request = rf.get("/")

    middleware = SessionValidationMiddleware(lambda r: None)

    response = middleware(request)

    assert response is None