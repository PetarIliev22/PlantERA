import customtkinter as ctk
from ctkfontawesome import icon_to_image

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            width=250,
            corner_radius=0,
            fg_color="#0D1518"
        )

        self.parent = parent
        self.pack_propagate(False)
        
        self.provision_button = self.create_menu_button(
            "microchip",
            "Provision Device"
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
        
        self.footer_text = ctk.CTkLabel(
            self,
            text="© 2026 Plantera Software",
            font=ctk.CTkFont(
                family="Arial",
                size=12
            ),
            text_color="#7E948F"
        )

        self.footer_text.pack(
            side="bottom",
            pady=20
        )
        
    def create_menu_button(self, icon, text):
        icon_image = icon_to_image(
            icon,
            scale_to_width=18,
            fill="#DCE5E3"
        )
        
        button = ctk.CTkButton(
            self,
            image=icon_image,
            text=text,
            height=62,
            corner_radius=12,
            fg_color="transparent",
            hover_color="#162A26",
            text_color="#DCE5E3",
            font=ctk.CTkFont(
                family="Arial",
                size=14,
                weight="bold"
                
            ),
            anchor="w"
        )

        button.pack(
            fill="x",
            padx=20,
            pady=5
        )

        return button
    
            
        