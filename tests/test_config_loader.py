from config.config_loader import load_config


def test_load_config():
    config = load_config("device_connection.json")

    assert "status" in config
    assert "button" in config