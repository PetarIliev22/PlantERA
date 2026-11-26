import asyncio
import pytest
from types import SimpleNamespace
from unittest.mock import Mock, AsyncMock, call
from handlers.auth_handler.register_handler import RegisterHandler

@pytest.mark.parametrize(
    "avatar_data, avatar_error",
    [
        (None, None),
        (b"image_data", None),
        (b"image_data", RuntimeError("Upload failed")),
    ],
)
def test_register_success(avatar_data, avatar_error, monkeypatch):
    handler = Mock()
    register = handler.view.register

    register.first_name.text.return_value = "Test"
    register.last_name.text.return_value = "User"
    register.email.text.return_value = "user@example.com"
    register.password.text.return_value = "password123"
    register.confirm.text.return_value = "password123"
    register.avatar_data = avatar_data

    handler.validate.return_value = None

    handler.messages = {
        "register": {},
        "general": {
            "unexpected_error": "unexpected_error",
            "network_error": "network_error",
        },
    }

    user = SimpleNamespace(id="test-user-id")

    sign_up = AsyncMock(
        return_value=SimpleNamespace(
            user=user,
            session=True,
        )
    )

    update_avatar = AsyncMock(side_effect=avatar_error)

    monkeypatch.setattr(
        "services.supabase.supabase_auth.sign_up",
        sign_up,
    )

    monkeypatch.setattr(
        "services.supabase.supabase_queries.update_user_avatar",
        update_avatar,
    )

    asyncio.run(
        RegisterHandler.handle_register.__wrapped__(handler)
    )

    sign_up.assert_awaited_once_with(
        "user@example.com",
        "password123",
        "Test",
        "User",
    )

    handler.authenticated.emit.assert_called_once_with(user)
    handler.view.set_loading.assert_called_once_with(True)
    handler.view.alert.show_message.assert_not_called()

    if avatar_data:
        update_avatar.assert_awaited_once_with(
            user.id, avatar_data
        )
    else:
        update_avatar.assert_not_awaited()
        
@pytest.mark.parametrize(
    "user_exists, error, expected, success",
    [
        (True, None, "success", True),
        (False, None, "unexpected_error", False),
        (False, ConnectionError(), "network_error", False),
        (False, RuntimeError(), "unexpected_error", False),
    ],
)
def test_register_without_session(
    user_exists, error, expected, success, monkeypatch
):
    handler = Mock()
    register = handler.view.register

    register.first_name.text.return_value = "Test"
    register.last_name.text.return_value = "User"
    register.email.text.return_value = "user@example.com"
    register.password.text.return_value = "password123"
    register.confirm.text.return_value = "password123"
    register.avatar_data = None

    handler.validate.return_value = None

    handler.messages = {
        "register": {
            "success": "success",
        },
        "general": {
            "unexpected_error": "unexpected_error",
            "network_error": "network_error",
        },
    }

    sign_up = AsyncMock(
        return_value=SimpleNamespace(
            user=Mock() if user_exists else None,
            session=None,
        ),
        side_effect=error,
    )

    update_avatar = AsyncMock()

    monkeypatch.setattr(
        "services.supabase.supabase_auth.sign_up",
        sign_up,
    )

    monkeypatch.setattr(
        "services.supabase.supabase_queries.update_user_avatar",
        update_avatar,
    )

    asyncio.run(
        RegisterHandler.handle_register.__wrapped__(handler)
    )

    handler.authenticated.emit.assert_not_called()
    update_avatar.assert_not_awaited()

    assert handler.view.set_loading.call_args_list == [
        call(True),
        call(False),
    ]

    if success:
        handler.view.switch_page.assert_called_once_with(0)
        handler.view.alert.show_message.assert_called_once_with(
            expected, success=True
        )
    else:
        handler.view.switch_page.assert_not_called()
        handler.view.alert.show_message.assert_called_once_with(
            expected
        )