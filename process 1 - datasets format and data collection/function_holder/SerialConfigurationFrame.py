import tkinter as tk
from tkinter import scrolledtext


class SerialConfigurationsFrame(tk.LabelFrame):
    def __init__(self, master, title="", *args, **kwargs):
        super().__init__(master, text=title, *args, **kwargs)

        self.PORT1_label = tk.Label(self, text="PORT 1 : ")
        self.PORT1_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.PORT1_entry = tk.Entry(self)
        self.PORT1_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.PORT2_label = tk.Label(self, text="PORT 2 : ")
        self.PORT2_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.PORT2_entry = tk.Entry(self)
        self.PORT2_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Serial monitor
        self.PORT1_serial_label = tk.Label(
            self, text="Serial Monitor for PORT 1")
        self.PORT1_serial_label.grid(
            row=3, column=0, padx=5, pady=5, sticky="w")
        self.PORT1_serial_entry = tk.Entry(self)
        self.PORT1_serial_entry.grid(
            row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.PORT2_serial_label = tk.Label(
            self, text="Serial Monitor for PORT 2")
        self.PORT2_serial_label.grid(
            row=3, column=2, padx=5, pady=5, sticky="w")
        self.PORT2_serial_entry = tk.Entry(self)
        self.PORT2_serial_entry.grid(
            row=4, column=2, columnspan=2, padx=5, pady=5, sticky="ew")


        # Increase width of PORT1_serial_entry
        self.PORT1_serial_entry.config(width=100)

        # Increase width of PORT2_serial_entry
        self.PORT2_serial_entry.config(width=100)  # Adjust width as needed