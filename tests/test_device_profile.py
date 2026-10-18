from ui.components.provision.device_profile import DeviceProfile

def test_find_profile():
    profile = DeviceProfile.find_profile(
        "ESP32-D0WD-V3"
    )

    assert profile is not None
    assert profile["name"] == "ESP32-D0WD-V3 Device Profile"