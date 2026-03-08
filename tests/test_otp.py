import pytest
from authentication.models import OtpCode


@pytest.mark.django_db
def test_otp_verify(api_client, user):

    otp = OtpCode.objects.create(
        user=user,
        code="123456"
    )

    response = api_client.post("/api/v1/auth/otp-verify/", {
        "email": "test@veloma.io",
        "code": "123456"
    })

    assert response.status_code == 200
    assert "reset_token" in response.data