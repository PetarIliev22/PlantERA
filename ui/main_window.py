import ctypes
import customtkinter as ctk

from ui.components.toolbar import Toolbar
from ui.components.sidebar import Sidebar
from ui.views.provision_view import ProvisionView


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.overrideredirect(True)
        self.geometry("1300x800")
        self.minsize(1300, 800)
        self.configure(fg_color="#101C1F")

        self.toolbar = Toolbar(self)
        self.toolbar.pack(fill="x", side="top")

        self.sidebar = Sidebar(self)
        self.sidebar.pack(fill="y", side="left")
        
        self.provision_view = ProvisionView(self)
        self.provision_view.pack(side="left", fill="both", expand=True)

        self.after(100, self.round_corners)

    def get_hwnd(self):
        return ctypes.windll.user32.GetParent(self.winfo_id())

    def round_corners(self):
        self.update_idletasks()

        region = ctypes.windll.gdi32.CreateRoundRectRgn(
            0,
            0,
            self.winfo_width() + 1,
            self.winfo_height() + 1,
            20,
            20
        )

        ctypes.windll.user32.SetWindowRgn(
            self.get_hwnd(),
            region,
            True
        )

    def remove_round_corners(self):
        ctypes.windll.user32.SetWindowRgn(
            self.get_hwnd(),
            0,
            True
        )