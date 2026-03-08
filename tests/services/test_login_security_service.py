import pytest
from services.auth.login_security_service import is_suspicious_login


@pytest.mark.django_db
def test_suspicious_login(user):

    result = is_suspicious_login(
        user=user,
        ip="8.8.8.8",
        country="US"
    )

    assert isinstance(result, bool)