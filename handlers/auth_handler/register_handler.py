import re
import asyncio
from PySide6.QtCore import QObject, Signal
from qasync import asyncSlot
from core.error_handler import is_network_error

class RegisterHandler(QObject):
    authenticated = Signal(object)

    def __init__(self, view):
        super().__init__(view)
        self.view = view
        self.messages = view.messages

    
    def validate(self, email, password, confirm, first_name, last_name):
        if not all((email, password, confirm, first_name, last_name)):
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
        alert = self.view.alert

        first_name = register.first_name.text().strip()
        last_name = register.last_name.text().strip()
        email = register.email.text().strip()
        password = register.password.text()
        confirm = register.confirm.text()
        avatar_data = register.avatar_data

        error = self.validate(email, password, confirm, first_name, last_name)

        if error:
            alert.show_message(messages[error])
            return

        self.view.set_loading(True)

        authenticated = False
        try:
            await asyncio.sleep(0)
            from services.supabase.supabase_auth import sign_up
            from services.supabase.supabase_queries import update_user_avatar
    
            response = await sign_up(email, password, first_name, last_name)
            if response.user and response.session:
                if avatar_data:
                    await update_user_avatar(response.user.id, avatar_data)

                authenticated = True
                self.authenticated.emit(response.user)
                
            elif response.user:
                self.view.switch_page(0)
                alert.show_message(messages["success"], success=True)

            else:
                alert.show_message(
                    self.messages["general"]["unexpected_error"]
                )

        except Exception as error:
            import httpx
            error_code = getattr(error, "code", None)

            if error_code in ("email_exists", "user_already_exists"):
                message = messages["email_exists"]

            elif is_network_error(error):
                message = self.messages["general"]["network_error"]

            else:
                message = self.messages["general"]["unexpected_error"]

            alert.show_message(message)

        finally:
            if not authenticated:
                self.view.set_loading(False)