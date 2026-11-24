from PySide6.QtGui import QImage, QPixmap, QPainter, QPainterPath
from PySide6.QtCore import Qt, QSize, QRectF, QBuffer, QIODevice

# Resize and center crop image
def _resize_image(image, size):
    image = image.scaled(
        size,
        Qt.AspectRatioMode.KeepAspectRatioByExpanding,
        Qt.TransformationMode.SmoothTransformation
    )

    x = (image.width() - size.width()) // 2
    y = (image.height() - size.height()) // 2

    return image.copy(x, y, size.width(), size.height())

# Compress image
def compress_image(file_path, size=256, quality=85):
    image = QImage(str(file_path))

    if image.isNull():
        raise ValueError("Invalid image file")

    image = _resize_image(image, QSize(size, size))

    buffer = QBuffer()

    if not buffer.open(QIODevice.OpenModeFlag.WriteOnly):
        raise ValueError("Failed to open image buffer")

    if not image.save(buffer, "JPEG", quality):
        raise ValueError("Image compression failed")

    return bytes(buffer.data())

# Create circular pixmap
def circular_pixmap(pixmap, size):
    pixmap = _resize_image(pixmap, size)

    result = QPixmap(size)
    result.fill(Qt.GlobalColor.transparent)

    path = QPainterPath()
    path.addEllipse(QRectF(result.rect()))

    painter = QPainter(result)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setClipPath(path)
    painter.drawPixmap(0, 0, pixmap)
    painter.end()

    return result