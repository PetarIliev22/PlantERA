import re
from PySide6.QtCore import QObject, Signal
from qasync import asyncSlot

class RegisterHandler(QObject):
    authenticated = Signal(object)

    def __init__(self, view):
        super().__init__(view)

        self.view = view
        self.messages = view.messages

        register_button = view.register.register_button
        register_button.clicked.connect(self.handle_register)

    def validate(self, email, password, confirm):
        if not email or not password or not confirm:
            return "empty_fields"

        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            return "invalid_email"

        if len(password) < 8:
            return "short_password"

        if password != confirm:
            return "password_mismatch"

        return None

    @asyncSlot()
    async def handle_register(self):
        register = self.view.register
        messages = self.messages["register"]
        button = register.register_button
        alert = self.view.alert

        email = register.email.text().strip()
        password = register.password.text()
        confirm = register.confirm.text()

        error = self.validate(email, password, confirm)

        if error:
            alert.show_message(messages[error])
            return

        button.setEnabled(False)
        button.setText(messages["loading"])

        try:
            from services.supabase.supabase_auth import sign_up

            response = await sign_up(email, password)

            if response.user and response.session:
                self.authenticated.emit(response.user)

            elif response.user:
                self.view.switch_page(0)
                alert.show_message(
                    messages["confirmation_required"],
                    success=True
                )

            else:
                alert.show_message(
                    self.messages["general"]["unexpected_error"]
                )

        except Exception as error:
            import httpx
            error_code = getattr(error, "code", None)

            if error_code in ("email_exists", "user_already_exists"):
                message = messages["email_exists"]

            elif isinstance(error, (ConnectionError, TimeoutError, OSError, httpx.ConnectError)):
                message = self.messages["general"]["network_error"]

            else:
                message = self.messages["general"]["unexpected_error"]

            alert.show_message(message)

        finally:
            button.setEnabled(True)
            button.setText(messages["button"])
