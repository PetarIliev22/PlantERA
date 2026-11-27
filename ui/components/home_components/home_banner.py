from html import escape
from ui.common.PySide6_Qt import *
from PySide6.QtCore import QDate
from utils.shadow import apply_shadow
from utils.svg_icons import svg_icon
from config.config_loader import load_config
from utils.avatar import set_avatar
from config.version import APP_VERSION

banner_config = load_config("home.json")["banner"]

class HomeBanner(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("homeBanner")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)

        self.create_ui()
        apply_shadow(self)

    def create_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 16, 24, 16)
        layout.setSpacing(20)

        profile = self.window().current_profile
        first_name = escape(profile.get("first_name") or "User")

        content = QVBoxLayout()
        content.setContentsMargins(0, 0, 0, 0)
        content.setSpacing(4)
        content.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        labels = [
            ("homeBannerSubtitle", banner_config["subtitle"]),
            ("homeBannerTitle",
             f'{escape(banner_config["title"])}, '
             f'<span style="color: #1687F8;">{first_name}!</span>'),
            ("homeBannerDescription", banner_config["description"])
        ]

        for name, text in labels:
            label = QLabel(text)
            label.setObjectName(name)
            label.setWordWrap(True)
            content.addWidget(label)

        separator = QFrame()
        separator.setObjectName("homeBannerSeparator")
        separator.setFixedWidth(1)

        information_container = QWidget()
        information_container.setObjectName("homeBannerInformation")
        information_container.setFixedWidth(150)
        information_container.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Maximum)

        information = QVBoxLayout(information_container)
        information.setContentsMargins(0, 0, 0, 0)
        information.setSpacing(8)

        values = {
            "role": profile["role"].capitalize(),
            "date": QDate.currentDate().toString("dd MMM yyyy"),
            "version": f"v{APP_VERSION}"
        }

        for key, item in banner_config["information"].items():
            information.addLayout(
                self.create_info_item(item["icon"], item["label"], values[key])
            )

        layout.addWidget(self.create_avatar(profile), 0, Qt.AlignmentFlag.AlignVCenter)
        layout.addLayout(content, 1)
        layout.addWidget(separator)
        layout.addWidget(information_container, 0, Qt.AlignmentFlag.AlignVCenter)

    def create_info_item(self, icon_name, label, value):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        icon = QLabel()
        icon.setFixedSize(20, 20)
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setPixmap(svg_icon(icon_name, "#1687F8", 18).pixmap(18, 18))

        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(0)

        for name, text in (("homeBannerInfoLabel", label), ("homeBannerInfoValue", value)):
            widget = QLabel(text)
            widget.setObjectName(name)
            widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
            text_layout.addWidget(widget)

        layout.addWidget(icon)
        layout.addLayout(text_layout, 1)

        return layout
    
    def create_avatar(self, profile):
        avatar = QLabel()
        avatar.setObjectName("homeBannerAvatar")
        avatar.setFixedSize(85, 85)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        set_avatar(avatar, profile, profile.get("avatar"), QSize(79, 79))

        return avatar