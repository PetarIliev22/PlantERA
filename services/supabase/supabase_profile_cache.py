from PySide6.QtCore import QSettings
from config.version import APP_NAME

def save_profile(user_id, first_name, last_name, email, avatar=None):
    settings = QSettings(APP_NAME, APP_NAME)

    settings.setValue("profile/user_id", user_id)
    settings.setValue("profile/first_name", first_name)
    settings.setValue("profile/last_name", last_name)
    settings.setValue("profile/email", email)
    settings.setValue("profile/avatar", avatar)
    settings.sync()

def load_profile():
    settings = QSettings(APP_NAME, APP_NAME)

    if not settings.contains("profile/user_id"):
        return None

    return {
        "user_id": settings.value("profile/user_id"),
        "first_name": settings.value("profile/first_name", ""),
        "last_name": settings.value("profile/last_name", ""),
        "email": settings.value("profile/email", ""),
        "avatar": settings.value("profile/avatar")
    }

def clear_profile():
    settings = QSettings(APP_NAME, APP_NAME)
    settings.remove("profile")
    settings.sync()