import customtkinter as ctk
from ctkfontawesome import icon_to_image
from serial.tools import list_ports
import serial


class ProvisionView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent"
        )

        self.serial_connection = None

        self.create_connection_card()
        self.refresh_ports()


    def create_connection_card(self):
        self.connection_card = ctk.CTkFrame(
            self,
            height=170,
            corner_radius=15,
            fg_color="#0D1518",
            border_width=1,
            border_color="#26363A"
        )

        self.connection_card.place(
            relx=0.02,
            rely=0.03,
            relwidth=0.47
        )

        self.connection_card.pack_propagate(False)

        self.create_connection_title()
        self.create_com_row()
        self.create_status_row()


    def create_connection_title(self):
        self.connection_title = ctk.CTkLabel(
            self.connection_card,
            text="Device Connection",
            image=icon_to_image(
                "link",
                scale_to_width=23,
                fill="#55D98A"
            ),
            compound="left",
            padx=10,
            font=ctk.CTkFont(
                family="Arial",
                size=17,
                weight="bold"
            ),
            text_color="#55D98A"
        )

        self.connection_title.pack(
            anchor="w",
            padx=10,
            pady=(16, 0)
        )


    def create_com_row(self):
        self.com_row = ctk.CTkFrame(
            self.connection_card,
            fg_color="transparent"
        )

        self.com_row.pack(
            fill="x",
            padx=14,
            pady=(16, 0)
        )

        self.com_label = ctk.CTkLabel(
            self.com_row,
            text="COM Port:",
            width=80,
            anchor="w",
            font=ctk.CTkFont(
                family="Arial",
                size=14
            ),
            text_color="#FFFFFF"
        )

        self.com_label.pack(side="left")

        self.com_box = ctk.CTkComboBox(
            self.com_row,
            values=[],
            height=35,
            corner_radius=9,
            border_width=1,
            state="readonly",
            border_color="#3B4B4F",
            fg_color="#182428",
            button_color="#182428",
            button_hover_color="#243438",
            dropdown_fg_color="#182428",
            dropdown_hover_color="#243438",
            text_color="#B1B1B1",
            font=ctk.CTkFont(
                family="Arial",
                size=14
            )
        )

        self.com_box.pack(
            side="left",
            fill="x",
            expand=True
        )

        self.com_box.set("No device selected")

        self.refresh_button = ctk.CTkButton(
            self.com_row,
            text="",
            image=icon_to_image(
                "refresh",
                scale_to_width=15,
                fill="#55D98A"
            ),
            width=40,
            height=35,
            corner_radius=9,
            fg_color="#182428",
            hover_color="#243438",
            border_width=1,
            border_color="#3B4B4F",
            command=self.refresh_ports
        )

        self.refresh_button.pack(
            side="left",
            padx=(10, 15)
        )

        self.connect_button = ctk.CTkButton(
            self.com_row,
            text="Connect",
            width=115,
            height=35,
            corner_radius=9,
            fg_color="#176B3A",
            hover_color="#21854A",
            border_width=1,
            border_color="#2A8C50",
            text_color="#FFFFFF",
            command=self.connect_device,
            font=ctk.CTkFont(
                family="Arial",
                size=15
            )
        )

        self.connect_button.pack(side="left")


    def create_status_row(self):
        self.status_row = ctk.CTkFrame(
            self.connection_card,
            fg_color="transparent"
        )

        self.status_row.pack(
            fill="x",
            padx=14,
            pady=(12, 0)
        )

        self.status_label = ctk.CTkLabel(
            self.status_row,
            text="Status:",
            width=80,
            anchor="w",
            font=ctk.CTkFont(
                family="Arial",
                size=14
            ),
            text_color="#FFFFFF"
        )

        self.status_label.pack(side="left")

        self.status_dot = ctk.CTkLabel(
            self.status_row,
            text="●",
            width=20,
            font=ctk.CTkFont(
                family="Arial",
                size=17
            ),
            text_color="#667477"
        )

        self.status_dot.pack(side="left")

        self.status_text = ctk.CTkLabel(
            self.status_row,
            text="Disconnected",
            font=ctk.CTkFont(
                family="Arial",
                size=14
            ),
            text_color="#8E9B9A"
        )

        self.status_text.pack(
            side="left",
            padx=(5, 0)
        )


    def refresh_ports(self):
        ports = list_ports.comports()

        port_names = [
            f"{port.device} - {port.description}"
            for port in ports
        ]

        self.com_box.configure(values=port_names)

        if port_names:
            self.com_box.set(port_names[0])
        else:
            self.com_box.set("No devices found")


    def connect_device(self):
        # Ако вече е свързано -> Disconnect
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            self.serial_connection = None

            self.status_dot.configure(
                text_color="#667477"
            )

            self.status_text.configure(
                text="Disconnected",
                text_color="#8E9B9A"
            )

            self.connect_button.configure(
                text="Connect"
            )

            return

        # Connect
        selected = self.com_box.get()

        if not selected or selected == "No devices found":
            return

        port = selected.split(" - ")[0]

        try:
            self.serial_connection = serial.Serial(
                port=port,
                baudrate=115200,
                timeout=2
            )

            self.status_dot.configure(
                text_color="#55D98A"
            )

            self.status_text.configure(
                text="Connected",
                text_color="#55D98A"
            )

            self.connect_button.configure(
                text="Disconnect"
            )

        except serial.SerialException:
            self.serial_connection = None

            self.status_dot.configure(
                text_color="#E05A5A"
            )

            self.status_text.configure(
                text="Connection failed",
                text_color="#E05A5A"
            )

            self.connect_button.configure(
                text="Connect"
            )