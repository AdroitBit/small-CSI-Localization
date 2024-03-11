import tkinter as tk
from tkinter import scrolledtext
from function_holder.StartOrStopBtnFrame import *
from function_holder.ConfigurationsFrame import *

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Automatic Data Collector")
        self.master.geometry("800x600")
        # self.create_widgets()
        # self.create_layout()

        #create the button for the user 
        self.start_or_stop = StartOrStopBtnFrame(self.master)
        self.start_or_stop.pack(fill=tk.BOTH, padx=5, pady=5)

        self.configurations = ConfigurationsFrame(self.master, title="Data Collection Configurations")
        self.configurations.pack(fill=tk.BOTH, padx=5, pady=5,side=tk.TOP)


        #create the scrollable widget and append the data collecting configuration element to it
        # print(self.fuck)

    

root = tk.Tk()
app = App(root)
root.mainloop()
