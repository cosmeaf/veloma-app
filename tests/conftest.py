import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="test@veloma.io",
        email="test@veloma.io",
        password="Test123456"
    )


@pytest.fixture
def auth_client(api_client, user):

    response = api_client.post("/api/v1/auth/login/", {
        "email": "test@veloma.io",
        "password": "Test123456"
    })

    token = response.data["access"]

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {token}"
    )

    return api_client