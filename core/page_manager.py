
from importlib import import_module

from ui.PySide6_Qt import *
from config.config_loader import load_config

sidebarItems = load_config("sidebar.json")["sidebar"]

class PageManager(QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("mainPages")
        self.pages = {}

        self.create_pages()

    def create_pages(self):
        for item in sidebarItems:
            module_name, class_name = item["view"].rsplit(".", 1)

            module = import_module(f"ui.views.{module_name}")
            view_class = getattr(module, class_name)

            page = view_class(self)

            self.pages[item["name"]] = page
            self.addWidget(page)

        if self.count():
            self.setCurrentIndex(0)

    def change_page(self, name):
        page = self.pages.get(name)

        if page is not None:
            self.setCurrentWidget(page)
