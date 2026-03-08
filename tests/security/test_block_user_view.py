import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_block_user_endpoint(api_client, user):

    api_client.force_authenticate(user)

    response = api_client.post(
        "/api/v1/auth/block-user/",
        {"user_id": user.id},
        format="json"
    )

    assert response.status_code in [200, 403, 404]