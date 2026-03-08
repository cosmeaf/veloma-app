import pytest


@pytest.mark.django_db
def test_login_success(api_client, user):

    response = api_client.post(
        "/api/v1/auth/login/",
        {
            "email": "test@veloma.io",
            "password": "Test123456"
        },
        format="json"
    )

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_login_fail(api_client, user):

    response = api_client.post(
        "/api/v1/auth/login/",
        {
            "email": "test@veloma.io",
            "password": "wrong"
        },
        format="json"
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_login_rate_limit(api_client, user):

    # tenta várias vezes com senha errada
    for _ in range(10):

        api_client.post(
            "/api/v1/auth/login/",
            {
                "email": "test@veloma.io",
                "password": "wrong"
            },
            format="json"
        )

    response = api_client.post(
        "/api/v1/auth/login/",
        {
            "email": "test@veloma.io",
            "password": "wrong"
        },
        format="json"
    )

    assert response.status_code == 429