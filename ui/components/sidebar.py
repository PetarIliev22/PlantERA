import qtawesome as qta

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout
)


class Sidebar(QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.setObjectName("sidebar")
        self.setFixedWidth(250)

        self.create_ui()

    def create_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 5, 15, 20)
        layout.setSpacing(10)

        # Active indicator
        self.active_indicator = QFrame(self)
        self.active_indicator.setObjectName("activeIndicator")
        self.active_indicator.setGeometry(0, 5, 8, 54)

        # Menu
        menu_items = [
            ("provision", "fa6s.microchip", "Provision Device", True),
            ("firmware", "fa6s.download", "Firmware", False),
            ("security", "fa6s.lock", "Keys & Security", False),
            ("settings", "fa6s.gear", "Settings", False),
            ("about", "fa6s.circle-info", "About", False),
        ]

        self.buttons = {}

        for name, icon, text, active in menu_items:
            button = QPushButton(text)

            button.setObjectName("sidebarButton")
            button.setProperty("active", active)
            
            button.setFixedHeight(54)

            button.setIcon(
                qta.icon(
                    icon,
                    color="#1687F8" if active else "#8491A5"
                )
            )
            button.setIconSize(QSize(20, 20))
            
            button.setCursor(
                Qt.CursorShape.PointingHandCursor
            )

            self.buttons[name] = button
            layout.addWidget(button)

        layout.addStretch()

        # Footer
        self.footer_text = QLabel(
            "© 2026 Plantera Software"
        )

        self.footer_text.setObjectName("sidebarFooter")
        self.footer_text.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(self.footer_text)