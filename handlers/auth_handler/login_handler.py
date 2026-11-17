from PySide6.QtCore import QObject, Signal
from qasync import asyncSlot

class LoginHandler(QObject):
    authenticated = Signal(object)

    def __init__(self, view):
        super().__init__(view)

        self.view = view
        self.messages = view.messages

        login_button = view.login.login_button
        login_button.clicked.connect(self.handle_login)

    @asyncSlot()
    async def handle_login(self):
        login = self.view.login
        messages = self.messages["login"]
        button = login.login_button
        alert = self.view.alert

        email = login.email.text().strip()
        password = login.password.text()

        if not email or not password:
            alert.show_message(messages["empty_fields"])
            return

        button.setEnabled(False)
        button.setText(messages["loading"])

        try:
            from services.supabase.supabase_auth import sign_in

            response = await sign_in(email, password)

            if response.user and response.session:
                self.authenticated.emit(response.user)
            else:
                alert.show_message(messages["invalid_credentials"])

        except Exception as error:
            import httpx
            code = getattr(error, "code", None)

            if code == "invalid_credentials":
                message = messages["invalid_credentials"]
                
            elif isinstance(error, (ConnectionError, TimeoutError, OSError, httpx.RequestError)):
                message = self.messages["general"]["network_error"]
                
            else:
                message = self.messages["general"]["unexpected_error"]

            alert.show_message(message)

        finally:
            button.setEnabled(True)
            button.setText(messages["button"])

