from ui.common.PySide6_Qt import *
from config.version import APP_VERSION
from config.config_loader import load_config
from utils.animations import fade_in_widget
from utils.svg_icons import svg_icon
from utils.paths import resource_path
from ui.windows.updater_window import launch_updater

texts = load_config("update_dialog.json")

class UpdateDialog(QFrame):
    def __init__(self, parent, update):
        super().__init__(parent)
        self.update = update

        self.setObjectName("updateOverlay")
        self.setGeometry(parent.rect())

        # Main card
        self.card = QFrame(self)
        self.card.setObjectName("updateDialog")
        self.card.setFixedSize(900, 550)

        overlay_layout = QVBoxLayout(self)
        overlay_layout.setContentsMargins(10, 10, 10, 10)
        overlay_layout.addWidget(
            self.card,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Main content
        layout = QHBoxLayout(self.card)
        layout.setContentsMargins(35, 30, 25, 30)
        layout.setSpacing(25)

        # Left content
        left = QVBoxLayout()
        left.setSpacing(14)

        # Title
        self.title = QLabel("New Update Available")
        self.title.setObjectName("updateTitle")
        self.title.setWordWrap(True)

        # Description
        self.details = QLabel(
            "A new version of PlantERA is ready to install "
            "with improvements and bug fixes. "
            "Please update to the latest version."
        )
        self.details.setObjectName("updateDetails")
        self.details.setWordWrap(True)

        # Version information
        version_box = QFrame()
        version_box.setObjectName("updateVersionBox")

        version_layout = QHBoxLayout(version_box)
        version_layout.setContentsMargins(18, 14, 18, 14)
        version_layout.setSpacing(14)

        # Version SVG icon
        version_icon = QLabel()
        version_icon.setObjectName("updateVersionIcon")
        version_icon.setFixedSize(50, 50)
        version_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        version_icon.setPixmap(
            svg_icon("gear.svg", "#1687F8", 32).pixmap(32, 32)
        )

        # Version labels
        version_texts = QVBoxLayout()
        version_texts.setSpacing(8)

        self.new_version = QLabel(
            f"New version: v{update['version']}"
        )
        self.new_version.setObjectName("updateNewVersion")

        self.current_version = QLabel(
            f"Current version: v{APP_VERSION}"
        )
        self.current_version.setObjectName("updateCurrentVersion")

        version_texts.addWidget(self.new_version)
        version_texts.addWidget(self.current_version)

        version_layout.addWidget(version_icon)
        version_layout.addLayout(version_texts, 1)
        
        # What's New
        self.whats_new_title = QLabel("What's New")
        self.whats_new_title.setObjectName("updateWhatsNewTitle")

        self.whats_new = QScrollArea()
        self.whats_new.setObjectName("updateWhatsNew")
        self.whats_new.setWidgetResizable(True)
        self.whats_new.setFrameShape(QFrame.Shape.NoFrame)
        self.whats_new.setFixedHeight(130)
        self.whats_new.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        container = QWidget()
        container.setObjectName("updateWhatsNewContainer")

        items_layout = QVBoxLayout(container)
        items_layout.setContentsMargins(8, 8, 8, 8)
        items_layout.setSpacing(10)

        release_notes = update.get("release_notes", "")

        changes = [
            line.strip()[2:].strip()
            for line in release_notes.splitlines()
            if line.strip().startswith("- ")
        ]

        if not changes:
            changes = ["Improvements and bug fixes."]

        for change in changes:
            row = QHBoxLayout()
            row.setSpacing(10)

            icon = QLabel()
            icon.setFixedSize(20, 20)
            icon.setPixmap(
                svg_icon("circle-check.svg", "#39A878", 20).pixmap(20, 20)
            )

            label = QLabel(change)
            label.setObjectName("updateChangeText")
            label.setWordWrap(True)

            row.addWidget(icon)
            row.addWidget(label, 1)

            items_layout.addLayout(row)

        items_layout.addStretch()
        self.whats_new.setWidget(container)

        # Update button
        self.update_button = QPushButton(
            texts["buttons"]["update"]
        )
        self.update_button.setObjectName("updateButton")
        self.update_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )
        self.update_button.setFixedHeight(48)
        self.update_button.clicked.connect(self.start_update)

        # Later button
        self.later_button = QPushButton(
            texts["buttons"]["later"]
        )
        self.later_button.setObjectName("laterButton")
        self.later_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )
        self.later_button.setFixedHeight(48)
        self.later_button.clicked.connect(self.close)

        # Button layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)
        buttons_layout.addWidget(self.update_button)
        buttons_layout.addWidget(self.later_button)

        # Assemble left content
        left.addWidget(self.title)
        left.addWidget(self.details)
        left.addWidget(version_box)
        left.addWidget(self.whats_new_title)
        left.addWidget(self.whats_new)
        left.addStretch()
        left.addLayout(buttons_layout)

        # Right illustration
        self.image = QLabel()
        self.image.setObjectName("updateIllustration")
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)

        image_path = resource_path(
            "assets", "img", "update_dialog_img.png"
        )

        pixmap = QPixmap(str(image_path))

        self.image.setPixmap(
            pixmap.scaled(
                370,
                370,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )

        layout.addLayout(left, 1)
        layout.addWidget(self.image, 1)

    def start_update(self):
        launch_updater(self.update)
        self.window().close()

def show_update_dialog(parent, update):
    dialog = UpdateDialog(parent, update)

    def show_dialog():
        if not parent.isVisible():
            return

        dialog.raise_()
        dialog.show()
        fade_in_widget(dialog)

    QTimer.singleShot(500, show_dialog)

    return dialog
