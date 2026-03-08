import pytest
from authentication.models import ResetPasswordToken


@pytest.mark.django_db
def test_reset_password(api_client, user):

    token = ResetPasswordToken.objects.create(
        user=user
    )

    response = api_client.post("/api/v1/auth/reset-password/", {
        "token": str(token.token),
        "password": "NovaSenha123",
        "password2": "NovaSenha123"
    })

    assert response.status_code == 200