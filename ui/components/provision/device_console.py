
import qtawesome as qta

from ui.PySide6_Qt import *


class DeviceConsole(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("deviceConsoleCard")
        self.setFixedHeight(280)

        self.create_ui()

    def create_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 18)
        layout.setSpacing(12)

        self.create_header(layout)
        self.create_console(layout)

    def create_header(self, layout):
        row = QHBoxLayout()
        row.setSpacing(10)

        icon = QLabel()
        icon.setPixmap(
            qta.icon(
                "fa6s.terminal",
                color="#1687F8"
            ).pixmap(20, 20)
        )

        title = QLabel("Device Console")
        title.setObjectName("deviceConsoleTitle")

        self.clear_button = QPushButton()
        self.clear_button.setObjectName("consoleClearButton")
        self.clear_button.setIcon(
            qta.icon(
                "fa6s.trash-can",
                color="#8491A5"
            )
        )
        self.clear_button.setText("Clear")
        self.clear_button.setFixedSize(85, 32)

        row.addWidget(icon)
        row.addWidget(title)
        row.addStretch()
        row.addWidget(self.clear_button)

        layout.addLayout(row)

    def create_console(self, layout):
        self.console = QPlainTextEdit()
        self.console.setObjectName("consoleOutput")
        self.console.setReadOnly(True)
        self.console.setPlaceholderText(
            "Device logs will appear here..."
        )

        self.console.setMaximumBlockCount(1000)
        self.console.setLineWrapMode(
            QPlainTextEdit.LineWrapMode.NoWrap
        )
        self.clear_button.clicked.connect(
            self.console.clear
        )

        layout.addWidget(self.console)

    def append_log(self, message):
        self.console.appendPlainText(str(message))

        scrollbar = self.console.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def clear_logs(self):
        self.console.clear()
