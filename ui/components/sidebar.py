import customtkinter as ctk
from ctkfontawesome import icon_to_image


class Sidebar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            width=250,
            corner_radius=0,
            fg_color="#FFFFFF"
        )

        self.parent = parent
        self.pack_propagate(False)
        
        self.active_indicator = ctk.CTkCanvas(
            self,
            width=8,
            height=54,
            bg="#FFFFFF",
            highlightthickness=0
        )

        self.active_indicator.place(
            x=0,
            y=5
        )

        self.active_indicator.create_polygon(
            0, 0,
            4, 2,
            7, 7,
            7, 47,
            4, 52,
            0, 54,
            fill="#1687F8",
            outline=""
        )
        
        # ACTIVE - Provision Device
        self.provision_button = self.create_menu_button(
            "microchip",
            "Provision Device",
            active=True
        )

        self.firmware_button = self.create_menu_button(
            "download",
            "Firmware"
        )

        self.security_button = self.create_menu_button(
            "lock",
            "Keys & Security"
        )

        self.settings_button = self.create_menu_button(
            "cog",
            "Settings"
        )

        self.about_button = self.create_menu_button(
            "info-circle",
            "About"
        )

        # Footer
        self.footer_text = ctk.CTkLabel(
            self,
            text="© 2026 Plantera Software",
            font=ctk.CTkFont(
                family="Arial",
                size=12
            ),
            text_color="#8491A5"
        )

        self.footer_text.pack(
            side="bottom",
            pady=20
        )

    def create_menu_button(
        self,
        icon,
        text,
        active=False
    ):
        if active:
            background_color = "#EAF4FF"
            hover_color = "#E1F0FF"
            text_color = "#1687F8"
            icon_color = "#1687F8"

        else:
            background_color = "transparent"
            hover_color = "#F1F6FC"
            text_color = "#8491A5"
            icon_color = "#8491A5"

        button = ctk.CTkButton(
            self,
            image=icon_to_image(
                icon,
                scale_to_width=18,
                fill=icon_color
            ),
            text=text,
            height=54,
            corner_radius=10,
            fg_color=background_color,
            hover_color=hover_color,
            text_color=text_color,
            font=ctk.CTkFont(
                family="Arial",
                size=14,
                weight="bold"
            ),
            anchor="w"
        )

        button.pack(
            fill="x",
            padx=15,
            pady=5
        )

        return button