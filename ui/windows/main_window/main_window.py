from qasync import asyncSlot
from ui.common.PySide6_Qt import *
from ui.components.toolbar import Toolbar
from ui.components.sidebar import Sidebar
from core.page_manager import PageManager
from ui.views.auth_views import AuthView
from ui.components.window_controls import WindowControls
from .window_events import WindowEvents
from .window_appearance import WindowAppearance
from .window_updates import WindowUpdates

class MainWindow(WindowEvents, WindowAppearance, WindowUpdates, QMainWindow):
    def __init__(self):
        super().__init__()

        self._closing = False
        self.update_worker = None
        
        self.setup_window()
        self.setup_timers()
        self.create_ui()

        self.window_controls = WindowControls(self)
        self.window_controls.show()

        self.position_window_controls()

    def create_ui(self):
        self.auth_view = AuthView(self)
        self.setCentralWidget(self.auth_view)

        self.auth_view.login_handler.authenticated.connect(
            self.on_authenticated
        )

        self.auth_view.register_handler.authenticated.connect(
            self.on_authenticated
        )

    @asyncSlot(object)
    async def on_authenticated(self, user):
        if hasattr(self, "page_manager"):
            return

        self.current_user = user

        try:
            await self.load_user_profile()
        except Exception:
            self.auth_view.switch_page(0)
            self.auth_view.submit_button.setEnabled(True)
            self.auth_view.login_tab.setEnabled(True)
            self.auth_view.register_tab.setEnabled(True)
            self.auth_view.alert.show_message(
                self.auth_view.messages["general"]["unexpected_error"]
            )
            return

        self.show_main_ui()
        self.start_update_check()

    async def load_user_profile(self):
        from services.supabase.supabase_queries import get_user_profile

        self.current_profile = await get_user_profile(
            self.current_user.id
        )
        
    def show_main_ui(self):
        central = QWidget()
        central.setObjectName("mainContainer")
        self.setCentralWidget(central)
        self.window_controls.raise_()

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = Sidebar(self)
        self.sidebar.profile.set_profile(self.current_profile, self.current_profile.get("avatar"))
        main_layout.addWidget(self.sidebar)

        right_container = QWidget()
        right_container.setObjectName("mainContent")

        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        self.toolbar = Toolbar(self)
        right_layout.addWidget(self.toolbar)

        self.page_manager = PageManager(right_container)
        right_layout.addWidget(self.page_manager, 1)

        self.sidebar.page_changed.connect(
            self.page_manager.change_page
        )

        main_layout.addWidget(right_container, 1)

    def position_window_controls(self):
        self.window_controls.move(
            self.width() - self.window_controls.width(),
            0
        )
        self.window_controls.raise_()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        if hasattr(self, "window_controls"):
            self.position_window_controls()

    def closeEvent(self, event):
        self._closing = True
        self.usb_timer.stop()

        if self.update_worker and self.update_worker.isRunning():
            event.ignore()
            return

        super().closeEvent(event)