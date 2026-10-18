
from importlib import import_module

from ui.PySide6_Qt import *
from config.config_loader import load_config

sidebarItems = load_config("sidebar.json")["sidebar"]

class PageManager(QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("mainPages")
        self.pages = {}

        if sidebarItems:
            self.change_page(sidebarItems[0]["name"])

   
    def get_or_create_page(self, name):
        page = self.pages.get(name)

        if page is None:
            item = next(
                (item for item in sidebarItems if item["name"] == name),
                None
            )

            if item is None:
                return None

            module_name, class_name = item["view"].rsplit(".", 1)
            module = import_module(f"ui.views.{module_name}")

            view_class = getattr(module, class_name)
            page = view_class(self)

            self.pages[name] = page
            self.addWidget(page)

        return page

    def change_page(self, name):
        page = self.get_or_create_page(name)

        if page is not None:
            self.setCurrentWidget(page)

