import pytest


@pytest.mark.django_db
def test_me_endpoint(auth_client, user):

    response = auth_client.get(f"/api/v1/auth/me/{user.id}/")

    assert response.status_code == 200
    assert response.data["email"] == "test@veloma.io"