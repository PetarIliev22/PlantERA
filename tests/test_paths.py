from utils.paths import resource_path

def test_resource_path():
    path = resource_path(
        "assets",
        "img",
        "boards",
        "esp32_board.png"
    )

    assert path.exists()