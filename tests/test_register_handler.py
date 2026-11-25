import pytest
from handlers.auth_handler.register_handler import RegisterHandler

@pytest.mark.parametrize(
    "email, password, confirm, expected",
    [
        ("user@example.com", "password123", "password123", None),
        ("", "password123", "password123", "empty_fields"),
        ("invalid-email", "password123", "password123", "invalid_email"),
        ("user@example.com", "123", "123", "short_password"),
        ("user@example.com", "password123", "password456", "password_mismatch"),
    ],
)
def test_register_validation(email, password, confirm, expected):
    result = RegisterHandler.validate(
        None, email, password, confirm, "Test", "User"
    )

    assert result == expected