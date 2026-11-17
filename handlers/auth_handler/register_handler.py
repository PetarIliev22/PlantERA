import re
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QMessageBox
from qasync import asyncSlot
from services.supabase.supabase_auth import sign_up
from config.config_loader import load_config

class RegisterHandler(QObject):
    authenticated = Signal(object)

    def __init__(self, view):
        super().__init__(view)
        self.view = view
        self.messages = load_config("auth_messages.json")

        self.view.register.register_button.clicked.connect(
            self.handle_register
        )

    @asyncSlot()
    async def handle_register(self):
        email = self.view.register.email.text().strip()
        password = self.view.register.password.text()
        confirm = self.view.register.confirm.text()

        messages = self.messages["register"]
        button = self.view.register.register_button

        if not email or not password or not confirm:
            QMessageBox.warning(
                self.view, messages["button"], messages["empty_fields"]
            )
            return

        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            QMessageBox.warning(
                self.view, messages["button"], messages["invalid_email"]
            )
            return

        if len(password) < 8:
            QMessageBox.warning(
                self.view, messages["button"], messages["short_password"]
            )
            return

        if password != confirm:
            QMessageBox.warning(
                self.view, messages["button"], messages["password_mismatch"]
            )
            return

        button.setEnabled(False)
        button.setText(messages["loading"])

        try:
            response = await sign_up(email, password)

            if response.user:
                if response.session:
                    self.authenticated.emit(response.user)
                else:
                    QMessageBox.information(
                        self.view,
                        messages["button"],
                        messages["confirmation_required"]
                    )
                    self.view.switch_page(0)
            else:
                QMessageBox.warning(
                    self.view,
                    messages["button"],
                    self.messages["general"]["unexpected_error"]
                )

        except Exception as error:
            code = getattr(error, "code", None)

            if code in ("email_exists", "user_already_exists"):
                message = messages["email_exists"]
            elif isinstance(error, (ConnectionError, TimeoutError, OSError)):
                message = self.messages["general"]["network_error"]
            else:
                message = self.messages["general"]["unexpected_error"]

            QMessageBox.warning(
                self.view,
                messages["button"],
                message
            )

        finally:
            button.setEnabled(True)
            button.setText(messages["button"])
