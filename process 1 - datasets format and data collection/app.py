import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import os

class App:
    def __init__(self, master):
        self.master = master
        master.title("UI with Data Collection, Image Display, and Serial Monitors")

        # Default folder directory
        self.folder_dir = os.path.dirname(os.path.abspath(__file__))

        # Folder directory input
        folder_frame = ttk.LabelFrame(master, text="Folder Directory")
        folder_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.folder_dir_entry = ttk.Entry(folder_frame, width=50)
        self.folder_dir_entry.grid(row=0, column=0, sticky="ew")
        self.folder_dir_entry.insert(0, self.folder_dir)

        # Port configurations
        port_frame = ttk.LabelFrame(master, text="Port Configurations")
        port_frame.grid(row=1, column=0, columnspan=2, sticky="ew")

        self.port1_entry = ttk.Entry(port_frame, width=20)
        self.port1_entry.grid(row=0, column=0, padx=5, pady=5)

        self.port2_entry = ttk.Entry(port_frame, width=20)
        self.port2_entry.grid(row=0, column=1, padx=5, pady=5)

        # Checkboxes for data collection, saving image
        options_frame = ttk.LabelFrame(master, text="Options")
        options_frame.grid(row=2, column=0, columnspan=2, sticky="ew")

        self.collect_data_var = tk.BooleanVar()
        self.collect_data_checkbox = ttk.Checkbutton(options_frame, text="Collect Data", variable=self.collect_data_var)
        self.collect_data_checkbox.grid(row=0, column=0, sticky="w")

        self.save_image_var = tk.BooleanVar()
        self.save_image_checkbox = ttk.Checkbutton(options_frame, text="Save Image Too", variable=self.save_image_var)
        self.save_image_checkbox.grid(row=1, column=0, sticky="w")

        # 4x4 table of checkboxes
        map_data_frame = ttk.LabelFrame(master, text="Map Data")
        map_data_frame.grid(row=3, column=0, columnspan=2, sticky="ew")

        self.map_data = []
        for i in range(4):
            for j in range(4):
                var = tk.BooleanVar()
                cb = ttk.Checkbutton(map_data_frame, variable=var)
                cb.grid(row=i, column=j, padx=5, pady=5)
                self.map_data.append(var)

        # Image display
        image_frame = ttk.LabelFrame(master, text="Image Display")
        image_frame.grid(row=4, column=0, columnspan=2, sticky="ew")

        self.image_label = ttk.Label(image_frame)
        self.image_label.grid(row=0, column=0, sticky="ew")

        # Serial Monitors
        serial_frame = ttk.LabelFrame(master, text="Serial Monitors")
        serial_frame.grid(row=5, column=0, columnspan=2, sticky="ew")

        self.serial_monitor1_text = tk.Text(serial_frame, height=10, width=50)
        self.serial_monitor1_text.grid(row=0, column=0, padx=5, pady=5)

        self.serial_monitor2_text = tk.Text(serial_frame, height=10, width=50)
        self.serial_monitor2_text.grid(row=0, column=1, padx=5, pady=5)

        # Initialize webcam
        self.capture = cv2.VideoCapture(0)  # Change 0 to the appropriate index if multiple webcams are connected
        self.update_image()

        # Make rows and columns expand with the window
        for i in range(6):  # Modify the range based on the number of rows
            master.rowconfigure(i, weight=1)
        for j in range(2):  # Modify the range based on the number of columns
            master.columnconfigure(j, weight=1)

    def update_image(self):
        ret, frame = self.capture.read()
        if ret:
            # Convert OpenCV image format (BGR) to Pillow format (RGB)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert Pillow image to Tkinter PhotoImage
            img = Image.fromarray(frame_rgb)
            img_tk = ImageTk.PhotoImage(image=img)
            # Update image label
            self.image_label.configure(image=img_tk)
            self.image_label.image = img_tk
            # Call update_image again after 10 milliseconds (adjust as needed)
            self.master.after(10, self.update_image)

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
