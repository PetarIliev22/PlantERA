from PySide6.QtGui import QPixmap
from PySide6.QtCore import QSize
from utils.compress_image import circular_pixmap

def set_avatar(label, profile, image_data=None, size=None):
    label.clear()

    if image_data:
        pixmap = QPixmap()

        if pixmap.loadFromData(image_data):
            label.setPixmap(
                circular_pixmap(pixmap, size or label.size())
            )
            return

    name = f"{profile['first_name']} {profile['last_name']}".strip()
    initials = "".join(part[0].upper() for part in name.split()[:2])

    label.setText(initials or "?")