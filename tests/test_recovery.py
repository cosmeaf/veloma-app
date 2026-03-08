import pytest
from authentication.models import OtpCode


@pytest.mark.django_db
def test_recovery(api_client, user):

    response = api_client.post("/api/v1/auth/recovery/", {
        "email": "test@veloma.io"
    })

    assert response.status_code == 200
    assert OtpCode.objects.count() == 1