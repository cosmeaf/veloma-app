import pytest
from services.tasks import send_email_task


@pytest.mark.django_db
def test_send_email_task(mailoutbox):

    payload = {
        "subject": "Test Email",
        "text": "Hello world",
        "from_email": "noreply@test.com",
        "to": ["user@test.com"],
        "html": "<b>Hello world</b>",
        "attachments": [],
    }

    send_email_task(payload)

    assert len(mailoutbox) == 1
    assert mailoutbox[0].subject == "Test Email"
    assert mailoutbox[0].to == ["user@test.com"]