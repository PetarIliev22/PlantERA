import ctypes
import customtkinter as ctk

from ui.components.toolbar import Toolbar
from ui.components.sidebar import Sidebar

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.overrideredirect(True)

        self.geometry("1300x700")
        self.minsize(1300, 800)
        self.configure(fg_color="#101C1F")

        # Toolbar
        self.toolbar = Toolbar(self)
        self.toolbar.pack(
            fill="x",
            side="top"
        )
        
        # Sidebar
        self.sidebar = Sidebar(self)
        self.sidebar.pack(
            fill="y",
            side="left"
        )

        self.after(100, self.round_corners)


    def round_corners(self):
        self.update_idletasks()

        width = self.winfo_width()
        height = self.winfo_height()
        radius = 20

        hwnd = ctypes.windll.user32.GetParent(
            self.winfo_id()
        )

        region = ctypes.windll.gdi32.CreateRoundRectRgn(
            0,
            0,
            width + 1,
            height + 1,
            radius,
            radius
        )

        ctypes.windll.user32.SetWindowRgn(
            hwnd,
            region,
            True
    )
        
    def remove_round_corners(self):
        hwnd = ctypes.windll.user32.GetParent(
            self.winfo_id()
        )

        ctypes.windll.user32.SetWindowRgn(
            hwnd,
            0,
            True
        )
        
        