import threading
from unittest.mock import Mock, patch
from services.device_service import DeviceService

def test_create_uid():
    mac = [0x20, 0x9B, 0xA9, 0x66, 0xE4, 0x9C]

    assert DeviceService.create_uid(mac) == "PC-9CE466A99B20"

def test_initial_state():
    service = DeviceService()

    assert service.is_running is False
    assert service.worker_thread is None
    assert service.stop_event is None
    
def test_stop():
    service = DeviceService()

    service.stop_event = threading.Event()
    service.stop()

    assert service.stop_event.is_set()
    
def test_start():
    service = DeviceService()

    with patch("services.device_service.threading.Thread") as mock_thread:
        result = service.start("COM3")

    assert result is True
    assert service.stop_event is not None
    assert service.worker_thread is mock_thread.return_value

    mock_thread.assert_called_once()
    mock_thread.return_value.start.assert_called_once()