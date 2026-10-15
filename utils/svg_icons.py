import re
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer

from utils.paths import resource_path

def svg_icon(filename, color="#8491A5", size=24):
    path = resource_path("assets", "img", "icons", filename)

    svg = path.read_text(encoding="utf-8")

    svg = re.sub(
        r'fill="(?!none)[^"]*"',
        f'fill="{color}"',
        svg
    )

    renderer = QSvgRenderer(svg.encode("utf-8"))

    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()

    return QIcon(pixmap)
