import httpx
import pytest

from core.error_handler import is_network_error

@pytest.mark.parametrize(
    "error",
    [
        ConnectionError(),
        TimeoutError(),
        httpx.ConnectError("Connection failed"),
        httpx.ReadTimeout("Request timed out"),
        httpx.ConnectTimeout("Connection timed out"),
        httpx.NetworkError("Network error"),
    ]
)
def test_network_errors(error):
    assert is_network_error(error) is True


@pytest.mark.parametrize(
    "error",
    [
        ValueError(),
        TypeError(),
        RuntimeError(),
        KeyError(),
        FileNotFoundError(),
        PermissionError(),
    ]
)
def test_non_network_errors(error):
    assert is_network_error(error) is False