import customtkinter as ctk
from ctkfontawesome import icon_to_image
from serial.tools import list_ports
from ui.dialogs.boot_dialog import BootDialog
import serial


class ProvisionView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.serial_connection = None

        self.create_connection_card()
        self.refresh_ports()

    def create_connection_card(self):
        self.connection_card = ctk.CTkFrame(
            self,
            height=170,
            corner_radius=15,
            fg_color="#FFFFFF",
            border_width=1,
            border_color="#D9E1EA"
        )
        self.connection_card.place(relx=0.02, rely=0.03, relwidth=0.47)
        self.connection_card.pack_propagate(False)

        self.create_title()
        self.create_com_row()
        self.create_status_row()

    def create_title(self):
        title = ctk.CTkLabel(
            self.connection_card,
            text="Device Connection",
            image=icon_to_image("link", scale_to_width=23, fill="#1687F8"),
            compound="left",
            padx=10,
            font=ctk.CTkFont("Arial", 17, "bold"),
            text_color="#1687F8"
        )
        title.pack(anchor="w", padx=10, pady=(16, 0))

    def create_com_row(self):
        row = ctk.CTkFrame(self.connection_card, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=(16, 0))

        ctk.CTkLabel(
            row,
            text="COM Port:",
            width=80,
            anchor="w",
            font=ctk.CTkFont("Arial", 14),
            text_color="#172033"
        ).pack(side="left")

        self.com_box = ctk.CTkComboBox(
            row,
            values=[],
            height=35,
            corner_radius=9,
            border_width=1,
            state="readonly",

            border_color="#D9E1EA",
            fg_color="#F5F7FA",

            button_color="#D9E1EA",
            button_hover_color="#1687F8",

            dropdown_fg_color="#919191",
            dropdown_hover_color="#1687F8",

            text_color="#738199",
            font=ctk.CTkFont("Arial", 14)
        )
        self.com_box.pack(side="left", fill="x", expand=True)
        self.com_box.set("No device selected")

        refresh_icon = icon_to_image(
            "refresh",
            scale_to_width=15,
            fill="#1687F8"
        )

        ctk.CTkButton(
            row,
            text="",
            image=refresh_icon,
            width=40,
            height=35,
            corner_radius=9,
            fg_color="#FFFFFF",
            hover_color="#EAF4FF",
            border_width=1,
            border_color="#D9E1EA",
            command=self.refresh_ports
        ).pack(side="left", padx=(10, 15))

        self.connect_button = ctk.CTkButton(
            row,
            text="Connect",
            width=115,
            height=35,
            corner_radius=9,
            fg_color="#1687F8",
            hover_color="#0878E8",
            text_color="#FFFFFF",
            font=ctk.CTkFont("Arial", 15, "bold"),
            command=self.connect_device
        )
        self.connect_button.pack(side="left")

    def create_status_row(self):
        row = ctk.CTkFrame(self.connection_card, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=(12, 0))

        ctk.CTkLabel(
            row,
            text="Status:",
            width=80,
            anchor="w",
            font=ctk.CTkFont("Arial", 14),
            text_color="#172033"
        ).pack(side="left")

        self.status_dot = ctk.CTkLabel(
            row,
            text="●",
            width=20,
            font=ctk.CTkFont("Arial", 17),
            text_color="#8A97AA"
        )
        self.status_dot.pack(side="left")

        self.status_text = ctk.CTkLabel(
            row,
            text="Disconnected",
            font=ctk.CTkFont("Arial", 14),
            text_color="#738199"
        )
        self.status_text.pack(side="left", padx=(5, 0))

    def refresh_ports(self):
        ports = [
            f"{port.device} - {port.description}"
            for port in list_ports.comports()
        ]

        self.com_box.configure(values=ports)
        self.com_box.set(ports[0] if ports else "No devices found")

    def set_status(self, text, color):
        self.status_dot.configure(text_color=color)
        self.status_text.configure(text=text, text_color=color)

    def connect_device(self):
        # Close old serial connection if open
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            self.serial_connection = None

        selected = self.com_box.get()

        if selected in ("", "No devices found", "No device selected"):
            return

        port = selected.split(" - ")[0]

        BootDialog(
            self.winfo_toplevel(),
            port,
            self.device_connected
        )
    def device_connected(self):
        self.set_status("Connected", "#22B573")
        self.connect_button.configure(text="Disconnect")