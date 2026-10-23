from importlib import import_module

from ui.common.PySide6_Qt import *
from config.config_loader import load_config
from utils.animations import fade_in_page

sidebarItems = load_config("sidebar.json")["sidebar"]

class PageManager(QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("mainPages")
        self.pages = {}
        
        self.page_configs = {
            item["name"]: item
            for item in sidebarItems
        }
        
        if sidebarItems:
            self.change_page(sidebarItems[0]["name"])

   
    def get_or_create_page(self, name):
        page = self.pages.get(name)
        
        if page is not None:
            return page

        item = self.page_configs.get(name)

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
            
            QTimer.singleShot(
                0,
                lambda: fade_in_page(page, 350)
                if self.currentWidget() is page else None
            )

