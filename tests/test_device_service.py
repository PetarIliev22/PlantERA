import sys
import pytest
import threading
from unittest.mock import Mock, patch
from services.device.device_service import DeviceService

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

    with patch("services.device.device_service.threading.Thread") as mock_thread:
        result = service.start("COM3")

    assert result is True
    assert service.stop_event is not None
    assert service.worker_thread is mock_thread.return_value

    mock_thread.assert_called_once()
    mock_thread.return_value.start.assert_called_once()
    
def test_esptool_import_failure(monkeypatch):
    monkeypatch.setitem(sys.modules, "esptool.cmds", None)

    service = Mock()
    stop_event = threading.Event()

    DeviceService.detect(service, "COM3", stop_event)

    service.failed.emit.assert_called_once()
    service.detected.emit.assert_not_called()
    
def test_detection_timeout(monkeypatch):
    service = Mock()
    service.DETECTION_TIMEOUT = 5.0
    service.RETRY_INTERVAL = 0.2

    stop_event = Mock()
    stop_event.is_set.return_value = False
    stop_event.wait.return_value = False

    detect_chip = Mock(
        side_effect=ConnectionError("Device not responding")
    )

    monkeypatch.setattr(
        "esptool.cmds.detect_chip",
        detect_chip
    )

    with patch("time.monotonic", side_effect=[0.0, 0.0, 4.9, 5.0]):
        DeviceService.detect(service, "COM3", stop_event)

    detect_chip.assert_called_once_with(
        "COM3", connect_attempts=1
    )

    stop_event.wait.assert_called_once_with(
        pytest.approx(0.1)
    )

    service.failed.emit.assert_called_once()
    service.detected.emit.assert_not_called()