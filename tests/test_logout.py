import pytest


@pytest.mark.django_db
def test_logout(auth_client):

    response = auth_client.post("/api/v1/auth/logout/")

    assert response.status_code == 200