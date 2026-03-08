import pytest


@pytest.mark.django_db
def test_register(api_client):

    response = api_client.post("/api/v1/auth/register/", {
        "email": "new@veloma.io",
        "password": "Test123456",
        "password2": "Test123456"
    })

    assert response.status_code == 201
    assert "access" in response.data
    assert response.data["user"]["email"] == "new@veloma.io"