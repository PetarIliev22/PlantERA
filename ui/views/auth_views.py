from ui.common.PySide6_Qt import *
from PySide6.QtGui import QPainter, QPixmap
from ui.components.auth_components.login import Login
from ui.components.auth_components.alert import Alert
from ui.components.auth_components.register import Register
from handlers.auth_handler.login_handler import LoginHandler
from handlers.auth_handler.register_handler import RegisterHandler
from utils.paths import resource_path
from utils.animations import fade_in_widget
from config.config_loader import load_config

class AuthView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("authView")

        self.background = QPixmap(str(resource_path(
            "assets", "img", "auth", "auth_background.png"
        )))
        self.scaled_background = QPixmap()
        self.create_ui()
        
        self.messages = load_config("auth_messages.json")
        self.login_handler = LoginHandler(self)
        self.register_handler = RegisterHandler(self)
        self.submit_button.clicked.connect(self.submit)

    def paintEvent(self, event):
        if self.scaled_background.isNull():
            super().paintEvent(event)
            return

        painter = QPainter(self)

        x = (self.scaled_background.width() - self.width()) // 2
        y = (self.scaled_background.height() - self.height()) // 2

        painter.drawPixmap(
            0, 0,
            self.scaled_background,
            x, y,
            self.width(), self.height()
        )
        
    def resizeEvent(self, event):
        super().resizeEvent(event)

        if not self.background.isNull():
            self.scaled_background = self.background.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
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
        self.alert = Alert()

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
        form.addWidget(self.alert)

        self.pages = QStackedWidget()

        self.login = Login()
        self.register = Register()

        self.pages.addWidget(self.login)
        self.pages.addWidget(self.register)

        form.addWidget(self.pages)
        self.submit_button = QPushButton("Login")
        self.submit_button.setObjectName("authSubmit")
        self.submit_button.setFixedHeight(48)
        self.submit_button.setCursor(Qt.CursorShape.PointingHandCursor)

        form.addWidget(self.submit_button)
        
        layout.addWidget(
            self.form,
            alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.login_tab.clicked.connect(lambda: self.switch_page(0))
        self.register_tab.clicked.connect(lambda: self.switch_page(1))

        self.switch_page(0)
        fade_in_widget(self.form)
        
        
    def submit(self):
        if self.pages.currentIndex() == 0:
            self.login_handler.handle_login()
        else:
            self.register_handler.handle_register()
            
    def switch_page(self, index):
        self.pages.setCurrentIndex(index)

        self.pages.setFixedHeight(
            self.pages.currentWidget().sizeHint().height()
        )

        self.login_tab.setChecked(index == 0)
        self.register_tab.setChecked(index == 1)

        self.submit_button.setText(
            "Login" if index == 0 else "Create Account"
        )
