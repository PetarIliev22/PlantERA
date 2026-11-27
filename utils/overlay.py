from PySide6.QtWidgets import QFrame

def show_overlay(parent, overlay=None):
    if overlay is None:
        overlay = QFrame(parent)

    overlay.setObjectName("dialogOverlay")
    overlay.setGeometry(parent.rect())
    overlay.show()
    overlay.raise_()

    return overlay


def remove_overlay(overlay):
    if overlay is not None:
        overlay.hide()
        overlay.deleteLater()