from ui.common.PySide6_Qt import *
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
from utils.avatar import set_avatar
from utils.shadow import apply_shadow
from utils.svg_icons import svg_icon

class UsersTable(QFrame):
    block_requested = Signal(dict)
    delete_requested = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("usersTableCard")
        self.create_ui()
        apply_shadow(self)

    def create_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        title_layout = QHBoxLayout()
        title_layout.setSpacing(8)
        title_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        icon = QLabel()
        icon.setFixedSize(24, 24)
        icon.setPixmap(svg_icon("user.svg", "#1687F8", 24).pixmap(24, 24))

        title = QLabel("All Users")
        title.setObjectName("usersTableTitle")

        title_layout.addWidget(icon, 0, Qt.AlignmentFlag.AlignVCenter)
        title_layout.addWidget(title, 0, Qt.AlignmentFlag.AlignVCenter)
        
        self.table = QTableWidget(0, 5)
        self.table.setObjectName("usersTable")
        self.table.setHorizontalHeaderLabels(["User", "Email", "Role", "Status", "Actions"])
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        vertical = self.table.verticalHeader()
        vertical.hide()
        vertical.setDefaultSectionSize(64)

        header = self.table.horizontalHeader()
        header.setFixedHeight(45)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

        for column, width in ((2, 160), (3, 120), (4, 120)):
            header.setSectionResizeMode(column, QHeaderView.ResizeMode.Fixed)
            self.table.setColumnWidth(column, width)

        for column in (0, 1):
            self.table.horizontalHeaderItem(column).setTextAlignment(
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
            )

        layout.addLayout(title_layout)
        layout.addWidget(self.table, 1)

    def set_users(self, users):
        self.table.setRowCount(len(users))

        for row, user in enumerate(users):
            blocked = user["is_blocked"]

            self.table.setCellWidget(row, 0, self.create_user_cell(user))
            self.table.setItem(row, 1, QTableWidgetItem(user["email"]))

            role = QTableWidgetItem(user["role"].capitalize())
            status = QTableWidgetItem("Blocked" if blocked else "Active")
            status.setForeground(QColor("#DC2626" if blocked else "#16A34A"))

            for column, item in ((2, role), (3, status)):
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, column, item)

            self.table.setCellWidget(row, 4, self.create_actions_cell(user))

    def create_user_cell(self, user):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(10)

        avatar = QLabel()
        avatar.setObjectName("usersTableAvatar")
        avatar.setFixedSize(40, 40)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        set_avatar(avatar, user, user.get("avatar"), QSize(36, 36))

        name = QLabel(f"{user['first_name']} {user['last_name']}".strip())
        name.setObjectName("usersTableName")
        name.setTextFormat(Qt.TextFormat.PlainText)

        layout.addWidget(avatar)
        layout.addWidget(name, 1)

        return container

    def create_actions_cell(self, user):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        blocked = user["is_blocked"]
        is_self = str(self.window().current_user.id) == str(user["id"])

        actions = (
            (
                "unlock.svg" if blocked else "lock.svg",
                "#16A34A" if blocked else "#D97706",
                "Unblock user" if blocked else "Block user",
                self.block_requested
            ),
            ("trash.svg", "#DC2626", "Delete user", self.delete_requested)
        )

        for icon, color, tooltip, signal in actions:
            button = QPushButton()
            button.setObjectName("usersActionButton")
            button.setFixedSize(34, 34)
            button.setIcon(svg_icon(icon, color, 18))
            button.setIconSize(QSize(18, 18))
            button.setToolTip(tooltip)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setEnabled(not is_self)
            button.clicked.connect(lambda checked=False, s=signal: s.emit(user))

            layout.addWidget(button)

        return container