
import webbrowser
from PySide6.QtWidgets import QMessageBox
from config.version import APP_VERSION

def show_update_dialog(parent, update):
    version = update["version"]

    reply = QMessageBox.question(
        parent,
        "PlantERA Update",
        f"Налична е нова версия: {version}\n\n"
        f"Текуща версия: {APP_VERSION}\n\n"
        "Искаш ли да отвориш страницата за актуализация?",
        QMessageBox.StandardButton.Yes |
        QMessageBox.StandardButton.No
    )

    if reply == QMessageBox.StandardButton.Yes:
        webbrowser.open(
            "https://github.com/"
            "PetarIliev22/PlantERA/releases/latest"
        )
