import tkinter as tk
from tkinter import ttk   
import os

class Image_frame:
    def __init__(self,master):
        self.master=master
        self.ttk=ttk.LabelFrame(master,text="Image Display")

        