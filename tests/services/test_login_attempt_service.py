import pytest
from services.auth.login_attempt_service import LoginAttemptService
from rest_framework.exceptions import Throttled


@pytest.mark.django_db
def test_block_after_max_attempts():

    email = "test@veloma.io"
    ip = "127.0.0.1"

    for _ in range(LoginAttemptService.MAX_ATTEMPTS):
        LoginAttemptService.register_failure(email, ip)

    with pytest.raises(Throttled):
        LoginAttemptService.guard(email, ip)