from ui.common.PySide6_Qt import *
from ui.views.auth_views import AuthView

class WindowUI:
    def show_auth_ui(self):
        self.auth_view = AuthView(self)
        self.setCentralWidget(self.auth_view)

        self.auth_view.login_handler.authenticated.connect(self.on_authenticated)
        self.auth_view.register_handler.authenticated.connect(self.on_authenticated)

    def show_main_ui(self):
        from ui.components.toolbar import Toolbar
        from ui.components.sidebar import Sidebar
        from core.page_manager import PageManager

        profile = self.current_profile
        role = profile["role"]

        central = QWidget()
        central.setObjectName("mainContainer")
        self.setCentralWidget(central)
        self.window_controls.raise_()

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = Sidebar(self, role)
        self.sidebar.profile.set_profile(profile, profile.get("avatar"))
        self.sidebar.profile.logout_requested.connect(self.handle_logout)

        main_layout.addWidget(self.sidebar)

        right_container = QWidget()
        right_container.setObjectName("mainContent")
        main_layout.addWidget(right_container, 1)

        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        self.toolbar = Toolbar(self)
        self.page_manager = PageManager(right_container, role)

        right_layout.addWidget(self.toolbar)
        right_layout.addWidget(self.page_manager, 1)

        self.sidebar.page_changed.connect(self.page_manager.change_page)