import asyncio
from qasync import asyncSlot
from ui.common.PySide6_Qt import *
from ui.dialogs.confirmation_dialog import ConfirmationDialog
from ui.components.users_components.users_summary import UsersSummary
from ui.components.users_components.users_table import UsersTable

class UsersView(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("usersView")
        self.create_ui()

        self.users_table.block_requested.connect(self.handle_block)
        self.users_table.delete_requested.connect(self.handle_delete)

        asyncio.get_running_loop().create_task(self.load_users())

    def create_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(24)

        self.users_summary = UsersSummary()
        self.users_table = UsersTable(self)

        layout.addLayout(self.users_summary)
        layout.addWidget(self.users_table, 1)

    async def load_users(self):
        from services.supabase.supabase_queries import get_users

        try:
            users = await get_users()
            self.users_summary.set_users(users)
            self.users_table.set_users(users)

        except Exception as error:
            QMessageBox.warning(self, "Users", f"Failed to load users:\n{error}")

    @asyncSlot(dict)
    async def handle_block(self, user):
        from services.supabase.supabase_queries import manage_user

        blocked = not user["is_blocked"]
        action = "Block" if blocked else "Unblock"

        await self.execute_action(action, user, manage_user, user["id"], user["role"], blocked)

    @asyncSlot(dict)
    async def handle_delete(self, user):
        from services.supabase.supabase_queries import delete_user
        await self.execute_action("Delete", user, delete_user, user["id"])

    async def execute_action(self, action, user, operation, *args):
        if not self.confirm_action(action, user):
            return

        self.users_table.setEnabled(False)

        try:
            await operation(*args)
            await self.load_users()

        except Exception as error:
            QMessageBox.warning(self, action, str(error))

        finally:
            self.users_table.setEnabled(True)

    def confirm_action(self, action, user):
        dialog = ConfirmationDialog(action, user, self)
        return dialog.exec() == QDialog.DialogCode.Accepted