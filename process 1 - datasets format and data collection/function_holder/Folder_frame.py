import tkinter as tk
from tkinter import ttk   
import os

class Folder_frame:
    def __init__(self,master):
        self.master=master
        self.folder_dir=os.getcwd()
        self.ttk = ttk.LabelFrame(master, text="Saving Location")
        self.folder_dir_entry = ttk.Entry(self.ttk,width=50)
        self.folder_dir_entry.grid(row=0,column=0,sticky="ew")
        self.folder_dir_entry.insert(0,self.folder_dir)
        
