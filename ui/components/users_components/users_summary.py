from ui.common.PySide6_Qt import *
from utils.svg_icons import svg_icon
from utils.shadow import apply_shadow

class UsersSummary(QHBoxLayout):
    def __init__(self):
        super().__init__()

        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(24)
        self.values = {}

        cards = [
            ("total", "Total Users", "user.svg", "#1687F8"),
            ("active", "Active Users", "circle-check.svg", "#16A34A"),
            ("blocked", "Blocked Users", "lock.svg", "#DC2626")
        ]

        for item in cards:
            self.addWidget(self.create_card(*item), 1)

    def create_card(self, key, title, icon_name, color):
        card = QFrame()
        card.setObjectName("usersSummaryCard")

        layout = QHBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(16)

        icon = QLabel()
        icon.setObjectName("usersSummaryIcon")
        icon.setFixedSize(48, 48)
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setPixmap(svg_icon(icon_name, color, 24).pixmap(24, 24))

        title_label = QLabel(title)
        title_label.setObjectName("usersSummaryTitle")

        value = QLabel("—")
        value.setObjectName("usersSummaryValue")
        self.values[key] = value

        details = QVBoxLayout()
        details.setSpacing(4)
        details.addWidget(title_label)
        details.addWidget(value)

        layout.addWidget(icon)
        layout.addLayout(details, 1)

        apply_shadow(card)
        return card

    def set_users(self, users):
        total = len(users)
        blocked = sum(user["is_blocked"] for user in users)

        self.values["total"].setText(str(total))
        self.values["active"].setText(str(total - blocked))
        self.values["blocked"].setText(str(blocked))