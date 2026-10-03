import customtkinter as ctk
from ctkfontawesome import icon_to_image


class Toolbar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            height=80,
            corner_radius=0,
            fg_color="#0D1518",
        )  

        self.bottom_line = ctk.CTkFrame(
            self,
            height=2,
            corner_radius=0,
            fg_color="#1E2527"
        )

        self.bottom_line.place(
            x=0,
            rely=1.0,
            relwidth=1.0,
            anchor="sw"
        )
        
        self.parent = parent
        self.pack_propagate(False)

        self.icons = {
            "close": icon_to_image(
                "xmark",
                scale_to_width=12,
                fill="#FFFFFF"
            ),
            "maximize": icon_to_image(
                "window-maximize",
                scale_to_width=12,
                fill="#FFFFFF"
            ),
            "minimize": icon_to_image(
                "window-minimize",
                scale_to_width=12,
                fill="#FFFFFF"
            )
        }

        self.logo_frame = ctk.CTkFrame(
            self,
            width=56,
            height=56,
            corner_radius=12,
            fg_color="#12372B"
        )

        self.logo_frame.pack(
            side="left",
            padx=(24, 16),
            pady=12
        )

        self.logo_frame.pack_propagate(False)

        self.title_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.title_frame.pack(
            side="left"
        )

        self.title_label = ctk.CTkLabel(
            self.title_frame,
            text="PlantERA - Provisioning Tool",
            font=ctk.CTkFont(
                family="Arial",
                size=20,
                weight="bold"
            )
        )

        self.title_label.pack(
            anchor="w"
        )

        self.subtitle_label = ctk.CTkLabel(
            self.title_frame,
            text="Prepare. Secure. Grow.",
            font=ctk.CTkFont(
                family="Arial",
                size=13
            ),
            text_color="#8E9B9A"
        )

        self.subtitle_label.pack(
            anchor="w"
        )

        self.close_button = self.create_button(
            "close",
            self.parent.destroy,
            hover_color="#C42B1C"
        )

        self.maximize_button = self.create_button(
            "maximize",
            self.toggle_maximize
        )

        self.minimize_button = self.create_button(
            "minimize",
            self.minimize_window
        )

        self.bind("<Button-1>", self.start_move)
        self.bind("<B1-Motion>", self.do_move)
        self.bind("<Double-Button-1>", self.toggle_maximize)

        self.title_frame.bind("<Button-1>", self.start_move)
        self.title_frame.bind("<B1-Motion>", self.do_move)
        self.title_frame.bind("<Double-Button-1>", self.toggle_maximize)

        self.title_label.bind("<Button-1>", self.start_move)
        self.title_label.bind("<B1-Motion>", self.do_move)
        self.title_label.bind("<Double-Button-1>", self.toggle_maximize)

        self.subtitle_label.bind("<Button-1>", self.start_move)
        self.subtitle_label.bind("<B1-Motion>", self.do_move)
        self.subtitle_label.bind("<Double-Button-1>", self.toggle_maximize)

    def create_button(self, icon, command, hover_color="#080F11"):
        button = ctk.CTkButton(
            self,
            text="",
            image=self.icons[icon],
            width=49,
            height=35,
            corner_radius=0,
            fg_color="transparent",
            hover_color=hover_color,
            command=command
        )

        button.pack(
            side="right",
            anchor="n"
        )

        return button

    def start_move(self, event):
        self.drag_x = event.x_root - self.parent.winfo_x()
        self.drag_y = event.y_root - self.parent.winfo_y()

    def do_move(self, event):
        if self.parent.state() == "zoomed":
            return

        x = event.x_root - self.drag_x
        y = event.y_root - self.drag_y

        self.parent.geometry(f"+{x}+{y}")

    def minimize_window(self):
        self.parent.overrideredirect(False)
        self.parent.iconify()

        self.parent.after(
            100,
            lambda: self.parent.overrideredirect(True)
        )

    def toggle_maximize(self, event=None):
        if self.parent.state() == "zoomed":
            self.parent.state("normal")

            self.parent.after(
                50,
                self.parent.round_corners
            )
        else:
            self.parent.remove_round_corners()
            self.parent.state("zoomed")