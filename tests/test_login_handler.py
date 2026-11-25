import asyncio
from types import SimpleNamespace
from unittest.mock import Mock, AsyncMock

import pytest

from handlers.auth_handler.login_handler import LoginHandler


@pytest.mark.parametrize(
    "email, password, success, error, expected",
    [
        ("", "", False, None, "empty_fields"),
        ("user@example.com", "password123", True, None, None),
        ("user@example.com", "wrong", False, None, "invalid_credentials"),
        ("user@example.com", "password123", False, ConnectionError(), "network_error"),
    ],
)
def test_login(email, password, success, error, expected, monkeypatch):
    handler = Mock()
    handler.view.login.email.text.return_value = email
    handler.view.login.password.text.return_value = password

    handler.messages = {
        "login": {
            "empty_fields": "empty_fields",
            "invalid_credentials": "invalid_credentials",
            "loading": "loading",
            "button": "login",
        },
        "general": {
            "network_error": "network_error",
            "unexpected_error": "unexpected_error",
        },
    }

    user = Mock()

    sign_in = AsyncMock(
        return_value=SimpleNamespace(
            user=user if success else None,
            session=success,
        ),
        side_effect=error,
    )

    monkeypatch.setattr(
        "services.supabase.supabase_auth.sign_in",
        sign_in,
    )

    asyncio.run(LoginHandler.handle_login.__wrapped__(handler))

    if success:
        handler.authenticated.emit.assert_called_once_with(user)
        handler.view.alert.show_message.assert_not_called()
    else:
        handler.view.alert.show_message.assert_called_once_with(expected)
        handler.authenticated.emit.assert_not_called()