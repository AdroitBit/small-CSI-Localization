import tkinter as tk
from tkinter import scrolledtext

class StartOrStopBtnFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)


        self.collecting=False;
        
        self.start_button = tk.Button(self, text="Start Collecting Data", command=self.start_collecting_data, bg='green')
        self.start_button.pack(fill=tk.BOTH, padx=5, pady=5, side=tk.LEFT)

        self.stop_button = tk.Button(self, text="Stop Collecting Data", command=self.stop_collecting_data, bg='red')
        self.stop_button.pack(fill=tk.BOTH, padx=5, pady=5, side=tk.LEFT)

        self.text_display = tk.Label(self, text=self.bool_to_str(self.collecting))
        self.text_display.pack(fill=tk.BOTH,padx=5,pady=5,side=tk.LEFT)

    def start_collecting_data(self):
        # self.start_button.config(bg='green')
        # self.stop_button.config(bg='red')
        # Add your data collection logic here
        self.collecting=True
        self.text_display.config(text=self.bool_to_str(self.collecting))


    def stop_collecting_data(self):
        # self.start_button.config(bg='red')
        # self.stop_button.config(bg='green')
        # self.start_button.config(bg='green')
        # self.stop_button.config(bg='red')
        # Add your stop data collection logic here
        self.collecting=False
        self.text_display.config(text=self.bool_to_str(self.collecting))
    def bool_to_str(self, bool):
        if bool:
            return "Collecting Data"
        else:
            return "Not Collecting Data"