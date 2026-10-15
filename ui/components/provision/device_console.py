from ui.PySide6_Qt import *
from datetime import datetime
from utils.svg_icons import svg_icon
from config.config_loader import load_config

console_config = load_config("device_console.json")

class DeviceConsole(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("deviceConsoleCard")
        self.setFixedHeight(270)

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
            svg_icon("terminal.svg", "#1687F8", 20).pixmap(20, 20)
        )

        title = QLabel("Device Console")
        title.setObjectName("deviceConsoleTitle")

        self.clear_button = QPushButton()
        self.clear_button.setObjectName("consoleClearButton")
        self.clear_button.setIcon(
            svg_icon("trash.svg", "#8491A5", 18)
        )
        self.clear_button.setIconSize(QSize(18, 18))
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
        self.console.setMaximumBlockCount(1000)
        self.console.setLineWrapMode(
            QPlainTextEdit.LineWrapMode.NoWrap
        )
        self.clear_button.clicked.connect(
            self.console.clear
        )

        layout.addWidget(self.console)

    def clear_logs(self):
        self.console.clear()

    def append_log(self, message, level=None):
        appearance = console_config["appearance"]

        if level is None:
            level = appearance["default_level"]

        level = level.upper()

        color = console_config["levels"].get(
            level,
            {"color": appearance["message_color"]}
        )["color"]

        timestamp = datetime.now().strftime("%H:%M:%S")

        cursor = self.console.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)

        # Timestamp
        timestamp_format = QTextCharFormat()
        timestamp_format.setForeground(
            QColor(appearance["timestamp_color"])
        )

        cursor.insertText(
            f"[{timestamp}] ",
            timestamp_format
        )

        # Level
        level_format = QTextCharFormat()
        level_format.setForeground(QColor(color))
        level_format.setFontWeight(QFont.Weight.Bold)

        cursor.insertText(
            f"[{level}] ",
            level_format
        )

        # Message
        message_format = QTextCharFormat()
        message_format.setForeground(
            QColor(appearance["message_color"])
        )

        cursor.insertText(
            str(message),
            message_format
        )

        cursor.insertBlock()

        self.console.setTextCursor(cursor)
        self.console.ensureCursorVisible()
        
    
    def log(self, key, level=None, **kwargs):
        message = console_config["messages"][key].format(
            **kwargs
        )

        self.append_log(message, level)


