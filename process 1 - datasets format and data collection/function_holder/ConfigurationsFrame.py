import tkinter as tk
from tkinter import scrolledtext
from function_holder.SerialConfigurationFrame import *


class ConfigurationsFrame(tk.LabelFrame):
    def __init__(self, master, title="", *args, **kwargs):
        super().__init__(master, text=title, *args, **kwargs)

        self.label_dir = tk.Label(self, text="Datasets saving directory:")
        self.label_dir.grid(row=0, column=0, columnspan=1,
                            padx=5, pady=5, sticky="w")
        # self.label_dir.pack(fill=tk.BOTH, padx=5, pady=5,side=tk.LEFT)
        self.saving_dir_entry = tk.Entry(self)
        self.saving_dir_entry.grid(
            row=0, column=1, padx=5, pady=5, sticky="ew")  # Changed column to 1 and added padx
        # self.saving_dir_entry.pack(fill=tk.BOTH,padx=5, pady=5,side=tk.LEFT)
        

        self.serial_config_frame = SerialConfigurationsFrame(
            self, title="Serial Configurations")
        self.serial_config_frame.grid(
            row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")  # Adjusted columnspan and sticky