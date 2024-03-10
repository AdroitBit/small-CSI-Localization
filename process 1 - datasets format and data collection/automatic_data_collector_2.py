import tkinter as tk
from tkinter import scrolledtext
from function_holder.ButtonFrame import *

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Automatic Data Collector")
        self.master.geometry("800x600")
        # self.create_widgets()
        # self.create_layout()

        #create the button for the user 
        self.button_frame = ButtonFrame(self.master)
        self.button_frame.pack(fill=tk.BOTH, padx=5, pady=5)


        #create the scrollable widget and append the data collecting configuration element to it
        print(self.fuck)

root = tk.Tk()
app = App(root)
root.mainloop()
