from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QLayout
from utils.svg_icons import svg_icon

def create_auth_field(layout: QLayout, label_text: str, placeholder: str, password: bool = False) -> QLineEdit:
    container = QWidget()
    container.setObjectName("authField")

    field_layout = QVBoxLayout(container)
    field_layout.setContentsMargins(0, 0, 0, 0)
    field_layout.setSpacing(3)

    label = QLabel(label_text)
    label.setObjectName("authFieldLabel")

    field = QLineEdit()
    field.setObjectName("authInput")
    field.setPlaceholderText(placeholder)
    field.setFixedHeight(44)

    if password:
        field.setEchoMode(QLineEdit.EchoMode.Password)

        eye = svg_icon("eye.svg", "#8492A6", 18)
        eye_off = svg_icon("eye-off.svg", "#8492A6", 18)

        toggle = QAction(eye_off, "", field)
        toggle.setCheckable(True)

        def toggle_password(checked):
            field.setEchoMode(
                QLineEdit.EchoMode.Normal if checked
                else QLineEdit.EchoMode.Password
            )
            toggle.setIcon(eye if checked else eye_off)

        toggle.toggled.connect(toggle_password)

        field.addAction(toggle, QLineEdit.ActionPosition.TrailingPosition)
        
    else:
        field.setClearButtonEnabled(True)

    field_layout.addWidget(label)
    field_layout.addWidget(field)
    layout.addWidget(container)

    return field