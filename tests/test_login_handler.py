import asyncio
from types import SimpleNamespace
from unittest.mock import Mock, AsyncMock, call

import pytest

from handlers.auth_handler.login_handler import LoginHandler


@pytest.mark.parametrize(
    "email, password, remember, success, error, expected",
    [
        ("", "", False, False, None, "empty_fields"),
        ("user@example.com", "password123", True, True, None, None),
        ("user@example.com", "password123", False, True, None, None),
        ("user@example.com", "wrong", False, False, None, "invalid_credentials"),
        ("user@example.com", "password123", False, False, ConnectionError(), "network_error"),
    ],
)
def test_login(email, password, remember, success, error, expected, monkeypatch):
    handler = Mock()

    handler.view.login.email.text.return_value = email
    handler.view.login.password.text.return_value = password
    handler.view.login.remember.isChecked.return_value = remember

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
            session=SimpleNamespace(
                access_token="test_access_token",
                refresh_token="test_refresh_token",
            ) if success else None,
        ),
        side_effect=error,
    )

    save_session = Mock()
    clear_session = Mock()

    monkeypatch.setattr(
        "services.supabase.supabase_auth.sign_in",
        sign_in,
    )

    monkeypatch.setattr(
        "services.supabase.supabase_session.save_session",
        save_session,
    )

    monkeypatch.setattr(
        "services.supabase.supabase_session.clear_session",
        clear_session,
    )

    asyncio.run(LoginHandler.handle_login.__wrapped__(handler))

    if success:
        handler.authenticated.emit.assert_called_once_with(user)
        handler.view.alert.show_message.assert_not_called()

        if remember:
            save_session.assert_called_once_with(
                "test_access_token",
                "test_refresh_token",
            )
            clear_session.assert_not_called()
        else:
            clear_session.assert_called_once_with()
            save_session.assert_not_called()

    else:
        handler.view.alert.show_message.assert_called_once_with(expected)
        handler.authenticated.emit.assert_not_called()

        save_session.assert_not_called()
        clear_session.assert_not_called()

    if not email or not password:
        handler.view.set_loading.assert_not_called()
        sign_in.assert_not_awaited()

    elif success:
        handler.view.set_loading.assert_called_once_with(True)

    else:
        assert handler.view.set_loading.call_args_list == [
            call(True),
            call(False),
        ]