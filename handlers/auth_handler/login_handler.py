import asyncio
from PySide6.QtCore import QObject, Signal
from core.error_handler import is_network_error
from qasync import asyncSlot

class LoginHandler(QObject):
    authenticated = Signal(object)

    def __init__(self, view):
        super().__init__(view)

        self.view = view
        self.messages = view.messages

    @asyncSlot()
    async def handle_login(self):
        login = self.view.login
        messages = self.messages["login"]
        alert = self.view.alert

        email = login.email.text().strip()
        password = login.password.text()
        remember = login.remember.isChecked()

        if not email or not password:
            alert.show_message(messages["empty_fields"])
            return
        
        self.view.set_loading(True)
        
        authenticated = False
        try:
            await asyncio.sleep(0)
            from services.supabase.supabase_auth import sign_in

            response = await sign_in(email, password)

            if response.user and response.session:
                from services.supabase.supabase_session import save_session
                
                if remember:
                    save_session(response.session.access_token, response.session.refresh_token)
                    
                authenticated = True
                self.authenticated.emit(response.user)
            else:
                alert.show_message(messages["invalid_credentials"])

        except Exception as error:
            code = getattr(error, "code", None)

            if code == "invalid_credentials":
                message = messages["invalid_credentials"]
                
            elif is_network_error(error):
                message = self.messages["general"]["network_error"]
                
            else:
                message = self.messages["general"]["unexpected_error"]

            alert.show_message(message)
            
        finally:
            if not authenticated:
                self.view.set_loading(False)