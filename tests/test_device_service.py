from services.device_service import DeviceService

def test_create_uid():
    mac = [0x20, 0x9B, 0xA9, 0x66, 0xE4, 0x9C]

    assert DeviceService.create_uid(mac) == "PC-9CE466A99B20"
