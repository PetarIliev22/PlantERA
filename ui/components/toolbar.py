import customtkinter as ctk
from ctkfontawesome import icon_to_image


class Toolbar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            height=80,
            corner_radius=0,
            fg_color="#FFFFFF"
        )

        self.parent = parent
        self.pack_propagate(False)

        self.icons = {
            name: icon_to_image(
                icon,
                scale_to_width=14,
                fill="#8491A5"
            )
            for name, icon in {
                "close": "xmark",
                "maximize": "window-maximize",
                "minimize": "window-minimize"
            }.items()
        }

        # Долна разделителна линия
        self.bottom_line = ctk.CTkFrame(
            self,
            height=2,
            corner_radius=0,
            fg_color="#E2E8F0"
        )
        self.bottom_line.place(
            x=0,
            rely=1.0,
            relwidth=1.0,
            anchor="sw"
        )

        # Лого
        self.logo_frame = ctk.CTkFrame(
            self,
            width=56,
            height=56,
            corner_radius=12,
            fg_color="#1687F8"
        )
        self.logo_frame.pack(
            side="left",
            padx=(24, 16),
            pady=12
        )
        self.logo_frame.pack_propagate(False)

        # Заглавия
        self.title_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.title_frame.pack(side="left")

        self.title_label = ctk.CTkLabel(
            self.title_frame,
            text="PlantERA - Provisioning Tool",
            font=ctk.CTkFont(
                family="Arial",
                size=20,
                weight="bold"
            ),
            text_color="#172033"
        )
        self.title_label.pack(anchor="w")

        self.subtitle_label = ctk.CTkLabel(
            self.title_frame,
            text="Prepare. Secure. Grow.",
            font=ctk.CTkFont(
                family="Arial",
                size=13
            ),
            text_color="#738199"
        )
        self.subtitle_label.pack(anchor="w")

        # Window controls
        self.close_button = self.create_button(
            "close",
            self.parent.destroy,
            "#E5484D"
        )

        self.maximize_button = self.create_button(
            "maximize",
            self.toggle_maximize
        )

        self.minimize_button = self.create_button(
            "minimize",
            self.minimize_window
        )

        self.bind_drag_events(
            self,
            self.title_frame,
            self.title_label,
            self.subtitle_label
        )

    def create_button(
        self,
        icon,
        command,
        hover_color="#F4F7FA"
    ):
        button = ctk.CTkButton(
            self,
            text="",
            image=self.icons[icon],
            width=50,
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

    def bind_drag_events(self, *widgets):
        for widget in widgets:
            widget.bind(
                "<Button-1>",
                self.start_move
            )

            widget.bind(
                "<B1-Motion>",
                self.do_move
            )

            widget.bind(
                "<Double-Button-1>",
                self.toggle_maximize
            )

    def start_move(self, event):
        self.drag_x = (
            event.x_root -
            self.parent.winfo_x()
        )

        self.drag_y = (
            event.y_root -
            self.parent.winfo_y()
        )

    def do_move(self, event):
        if self.parent.state() == "zoomed":
            return

        x = event.x_root - self.drag_x
        y = event.y_root - self.drag_y

        self.parent.geometry(
            f"+{x}+{y}"
        )

    def minimize_window(self):
        self.parent.overrideredirect(False)
        self.parent.iconify()

        self.parent.after(
            100,
            lambda:
            self.parent.overrideredirect(True)
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