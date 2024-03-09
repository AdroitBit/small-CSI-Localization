import tkinter as tk
import threading
import time



class SerialMonitorUI:
    def __init__(self, master):
        self.master = master
        
        # Title for the first text area
        self.label1 = tk.Label(master, text="Text Area 1", anchor="center")
        self.label1.grid(row=0, column=0, sticky="ew")
        
        # First text area
        self.text_area1 = tk.Text(master)
        self.text_area1.grid(row=1, column=0, sticky="nsew")
        
        # Title for the second text area
        self.label2 = tk.Label(master, text="Text Area 2", anchor="center")
        self.label2.grid(row=0, column=1, sticky="ew")
        
        # Second text area
        self.text_area2 = tk.Text(master)
        self.text_area2.grid(row=1, column=1, sticky="nsew")

    def update_text_area(self, port, data):
        if port == 1:
            text_area = self.text_area1
        elif port == 2:
            text_area = self.text_area2
        else:
            return

        text_area.insert(tk.END, data + "\n")
        text_area.see(tk.END)

root= tk.Tk()
root.title("Serial Monitor")
serial_monitor = SerialMonitorUI(root)
