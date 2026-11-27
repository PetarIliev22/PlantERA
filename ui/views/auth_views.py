from ui.common.PySide6_Qt import *
from ui.components.auth_components.login import Login
from ui.components.auth_components.alert import Alert
from ui.components.auth_components.register import Register
from handlers.auth_handler.login_handler import LoginHandler
from handlers.auth_handler.register_handler import RegisterHandler
from ui.components.auth_components.remembered_login import RememberedLogin
from ui.components.loading_spinner import LoadingSpinner
from ui.components.auth_components.blocked_login import BlockedLogin
from utils.paths import resource_path
from utils.animations import fade_in_widget
from config.config_loader import load_config

class AuthView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.blocked_login = None
        self.messages = load_config("auth_messages.json")
        
        self.setObjectName("authView")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.create_ui()

        self.login_handler = LoginHandler(self)
        self.register_handler = RegisterHandler(self)
        
        self.submit_button.clicked.connect(self.submit)

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

        self.tabs = QFrame()
        self.tabs.setObjectName("authTabs")

        tabs_layout = QHBoxLayout(self.tabs)
        tabs_layout.setContentsMargins(4, 4, 4, 4)
        tabs_layout.setSpacing(4)

        self.login_tab = QPushButton("Login")
        self.register_tab = QPushButton("Register")

        for button in (self.login_tab, self.register_tab):
            button.setObjectName("authTab")
            button.setCheckable(True)
            tabs_layout.addWidget(button)

        form.addWidget(self.tabs)
        form.addWidget(self.alert)

        self.pages = QStackedWidget()

        self.login = Login()
        self.register = Register()

        self.pages.addWidget(self.login)
        self.pages.addWidget(self.register)
        from services.supabase.supabase_profile_cache import load_profile

        profile = load_profile()

        self.remembered_login = None

        if profile is not None:
            self.remembered_login = RememberedLogin(profile)
            self.pages.addWidget(self.remembered_login)
            
        form.addWidget(self.pages)

        self.submit_button = QPushButton()
        self.submit_button.setObjectName("authSubmit")
        self.submit_button.setFixedHeight(48)
        self.submit_button.setCursor(Qt.CursorShape.PointingHandCursor)

        form.addWidget(self.submit_button)
        
        self.spinner = LoadingSpinner(size=48, color="#1687F8")

        form.addWidget(
            self.spinner,
            alignment=Qt.AlignmentFlag.AlignCenter
        )
        
        layout.addWidget(
            self.form,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.login_tab.clicked.connect(lambda: self.switch_page(0))
        self.register_tab.clicked.connect(lambda: self.switch_page(1))

        self.switch_page(2 if self.remembered_login is not None else 0)
        fade_in_widget(self.form)

    @property
    def is_login_page(self) -> bool:
        return self.pages.currentIndex() == 0
    
    @property
    def is_remembered_page(self) -> bool:
        return self.pages.currentIndex() == 2
    
    @property
    def current_messages(self) -> dict:
        return self.messages[
            "login" if self.is_login_page else "register"
        ]

    def submit(self):
        if self.is_login_page:
            self.login_handler.handle_login()
        else:
            self.register_handler.handle_register()

    def set_loading(self, loading: bool) -> None:
        for button in (
            self.submit_button,
            self.login_tab,
            self.register_tab
        ):
            button.setEnabled(not loading)

        self.submit_button.setText(
            self.current_messages["loading" if loading else "button"]
        )

    def show_blocked(self):
        if self.blocked_login is not None:
            return
        
        self.spinner.stop()
        self.form.hide()

        self.blocked_login = BlockedLogin(self)
        self.blocked_login.back_button.setEnabled(False)
        self.blocked_login.back_requested.connect(self.show_login)
        
        self.layout().addWidget(self.blocked_login, alignment=Qt.AlignmentFlag.AlignCenter)
    
    def show_login(self):
        self.blocked_login.hide()
        self.blocked_login.deleteLater()
        self.blocked_login = None

        self.login.password.clear()
        self.switch_page(0)
        self.set_loading(False)
        self.form.show()
    
    def switch_page(self, index: int) -> None:
        self.pages.setCurrentIndex(index)
        self.pages.setFixedHeight(self.pages.currentWidget().sizeHint().height())

        remembered = self.is_remembered_page
        
        self.tabs.setVisible(not remembered)
        self.submit_button.setVisible(not remembered)
        self.spinner.setVisible(remembered)

        self.login_tab.setChecked(self.is_login_page)
        self.register_tab.setChecked(index == 1)

        self.subtitle.setText(
            "Welcome back!" if index == 2
            else "Sign in to your PlantERA account"
        )

        if remembered:
            self.spinner.start()
        else:
            self.spinner.stop()
            self.submit_button.setText(self.current_messages["button"])