import tkinter as tk
from tkinter import ttk   
import os

class Ports_configuration_frame:
    def __init__(self,master):
        self.master=master
        self.ttk=ttk.LabelFrame(master,text="Port Configurations")

        self.PORT1_label=ttk.Label(self.ttk,text="Port 1")
        self.PORT1_label.grid(row=0,column=0,padx=5,pady=5)
        self.PORT1_entry=ttk.Entry(self.ttk,width=20)
        self.PORT1_entry.insert(0,"COM24")

        self.PORT1_entry.grid(row=0,column=1,padx=5,pady=5)
        self.PORT2_label=ttk.Label(self.ttk,text="Port 2")
        self.PORT2_label.grid(row=0,column=2,padx=5,pady=5)
        self.PORT2_entry=ttk.Entry(self.ttk,width=20)
        self.PORT2_entry.insert(0,"COM3")
        self.PORT2_entry.grid(row=0,column=3,padx=5,pady=5)

    
