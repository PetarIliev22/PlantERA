from ui.common.PySide6_Qt import *
from PySide6.QtGui import QPainter, QPixmap
from ui.components.auth_components.login import Login
from ui.components.auth_components.register import Register
from utils.paths import resource_path
from utils.animations import fade_in_widget
 
class AuthView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("authView")

        self.background = QPixmap(str(resource_path(
            "assets", "img", "auth", "auth_background.png"
        )))

        self.create_ui()

    def paintEvent(self, event):
        if self.background.isNull():
            super().paintEvent(event)
            return

        image = self.background.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )

        x = (image.width() - self.width()) // 2
        y = (image.height() - self.height()) // 2

        painter = QPainter(self)
        painter.drawPixmap(
            0, 0, image, x, y, self.width(), self.height()
        )

    def create_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.form = QFrame()
        self.form.setObjectName("authForm")
        self.form.setFixedWidth(480)

        form = QVBoxLayout(self.form)
        form.setContentsMargins(28, 26, 28, 26)
        form.setSpacing(12)

        self.logo = QLabel()
        self.logo.setObjectName("authLogo")
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo = QPixmap(str(resource_path(
            "assets", "img", "logo", "plantera_full_logo.png"
        )))

        self.logo.setPixmap(logo.scaled(
            230, 70,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))

        form.addWidget(self.logo)

        self.subtitle = QLabel("Sign in to your PlantERA account")
        self.subtitle.setObjectName("authSubtitle")
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        form.addWidget(self.subtitle)
        form.addSpacing(2)

        tabs = QFrame()
        tabs.setObjectName("authTabs")

        tabs_layout = QHBoxLayout(tabs)
        tabs_layout.setContentsMargins(4, 4, 4, 4)
        tabs_layout.setSpacing(4)

        self.login_tab = QPushButton("Login")
        self.register_tab = QPushButton("Register")

        for button in (self.login_tab, self.register_tab):
            button.setObjectName("authTab")
            button.setCheckable(True)
            tabs_layout.addWidget(button)

        form.addWidget(tabs)

        self.pages = QStackedWidget()

        self.login = Login()
        self.register = Register()

        self.pages.addWidget(self.login)
        self.pages.addWidget(self.register)

        form.addWidget(self.pages)

        layout.addWidget(
            self.form,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.login_tab.clicked.connect(lambda: self.switch_page(0))
        self.register_tab.clicked.connect(lambda: self.switch_page(1))

        self.switch_page(0)
        fade_in_widget(self.form)
        
    def switch_page(self, index):
        self.pages.setCurrentIndex(index)
        self.login_tab.setChecked(index == 0)
        self.register_tab.setChecked(index == 1)
