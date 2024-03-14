import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import cv2
from PIL import Image, ImageTk
import serial
import sys
import datetime
import json


ctk.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

def all_serial_ports():
    if sys.platform.startswith('win'):
        import serial.tools.list_ports
        ports=serial.tools.list_ports.comports()
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        import serial.tools.list_ports_posix
        ports=serial.tools.list_ports_posix.comports()
    elif sys.platform.startswith('darwin'):
        import serial.tools.list_ports_osx
        ports=serial.tools.list_ports_osx.comports()
    else:
        raise EnvironmentError('Unsupported platform')
    return map(lambda x: x.device, ports)
    # return map(lambda x: (x.device, x.description, x.hwid), ports)
    # for port, desc, hwid in sorted(ports):
    #     print(f"{port}: {desc} [{hwid}]")
    # return ports


class CollectStopFrame(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(
            master, 
            # border_width=2, 
            # border_color="red",
            width=200,
            height=2000
        )

        self.can_collect_var=ctk.BooleanVar(value=False)

        self.collect_radio=ctk.CTkRadioButton(self,text="Collect",variable=self.can_collect_var, value=True)
        self.collect_radio.pack(side=tk.LEFT, padx=5)
        
        self.pause_radio=ctk.CTkRadioButton(self,text="Stop",variable=self.can_collect_var, value=False)
        self.pause_radio.pack(side=tk.LEFT, padx=5)


class BrowsingFrame(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(
            master, 
            # border_width=2, 
            # border_color="red",
            width=200,
            height=2000
        )

        self.folder_label = ctk.CTkLabel(self, text="Datasets saving folder:")
        self.folder_label.pack(side=tk.LEFT, padx=5)

        self.folder_path = ctk.StringVar()
        default_folder_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),"test_datasets")
        if not os.path.exists(default_folder_path):
            os.makedirs(default_folder_path)
        self.folder_path.set(default_folder_path)
        
        self.folder_entry = ctk.CTkEntry(self, textvariable=self.folder_path, width=500)
        self.folder_entry.pack(side=tk.LEFT, padx=5)

        self.browse_button = ctk.CTkButton(self, text="Browse", command=self.browse_folder,width=50)
        self.browse_button.pack(side=tk.LEFT, padx=5)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory(initialdir=self.folder_path.get())
        if folder_selected:
            self.folder_path.set(folder_selected)

class MapDataFrame(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(
            master, 
            width=200,
            height=2000
        )

        self.map_data_label = ctk.CTkLabel(self, text="Map data :")
        self.map_data_label.pack(side=tk.TOP, padx=5, pady=5, anchor=tk.NW)
        
        self.checkboxes = []
        for i in range(4):
            frame = ctk.CTkFrame(self)
            frame.pack(side=tk.TOP, padx=5, pady=5, anchor=tk.NW)
            row_checkboxes = []
            for j in range(4):
                checkbox_var = ctk.IntVar()
                checkbox = ctk.CTkCheckBox(frame, text="", variable=checkbox_var, onvalue=1, offvalue=0, width=3)
                checkbox.pack(side=tk.LEFT, padx=2, pady=2)
                row_checkboxes.append(checkbox_var)
            self.checkboxes.append(row_checkboxes)
    def get_map_data(self):
        return [[checkbox.get() for checkbox in row] for row in self.checkboxes]

        

class CSICollectionConfigFrame(ctk.CTkFrame):
    def __init__(self,master=None):
        super().__init__(
            master, 
            # border_width=2, 
            # border_color="red",
            width=200,
            height=2000
        )

        self.csi_n_sample_frame=ctk.CTkFrame(self)
        self.csi_n_sample_frame.pack(side=tk.TOP, padx=5, pady=5, anchor=tk.NW)
        self.csi_n_sample_var = ctk.IntVar()
        self.csi_n_sample_var.set(20)
        self.csi_n_sample_label = ctk.CTkLabel(self.csi_n_sample_frame, text="sample of CSI data in used (csi_n_sample):")
        self.csi_n_sample_label.pack(side=tk.LEFT, padx=5, pady=5, anchor=tk.NW)
        self.csi_n_sample_entry = ctk.CTkEntry(self.csi_n_sample_frame, textvariable=self.csi_n_sample_var, width=40)
        self.csi_n_sample_entry.pack(side=tk.LEFT, padx=5, pady=5, anchor=tk.NW)

        self.flush_everytime_received_var = ctk.BooleanVar(value=True)
        self.flush_everytime_received_checkBox = ctk.CTkCheckBox(self, text="flush everytimes received csi_n_sample csi data", variable=self.flush_everytime_received_var, onvalue=True, offvalue=False)
        self.flush_everytime_received_checkBox.pack(side=tk.TOP, padx=5, pady=5,anchor=tk.W)

        self.clear_serial_monitor_everytime_received_var = ctk.BooleanVar(value=True)
        self.clear_serial_monitor_everytime_received_checkBox = ctk.CTkCheckBox(self, text="clear serial monitor everytime received csi_n_sample csi data", variable=self.clear_serial_monitor_everytime_received_var, onvalue=True, offvalue=False)
        self.clear_serial_monitor_everytime_received_checkBox.pack(side=tk.TOP, padx=5, pady=5,anchor=tk.W)



class AvailablePortsFrame(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(
            master, 
            # border_width=2, 
            # border_color="red",
            width=200,
            height=2000
        )

        self.ports_label = ctk.CTkLabel(self, text="Available Ports:")
        self.ports_label.pack(side=tk.LEFT, padx=5)

        self.ports_entry = ctk.CTkEntry(self, placeholder_text="Port")
        self.ports_entry.pack(side=tk.LEFT, padx=5)

        self.interval_ports_entry()
    def interval_ports_entry(self):
        self.ports_entry.delete(0, "end")
        self.ports_entry.insert(0, list(all_serial_ports()))
        self.after(100, self.interval_ports_entry)


class SerialMonitorFrame(ctk.CTkFrame):
    def __init__(self, master=None,placeholder_port="Port"):
        super().__init__(
            master, 
            # border_width=2, 
            # border_color="red",
            width=200,
            height=2000
        )

        self.port_entry = ctk.CTkEntry(self, placeholder_text=placeholder_port)
        self.port_entry.pack(side=tk.LEFT, padx=5)
        self.port_entry.bind("<Return>", self.connect_serial)#Return = enter pressed
        self.port_entry.bind("<FocusOut>", self.connect_serial)
        self.serialText=ctk.CTkTextbox(self,width=800,height=200,font=("monospace", 10))
        self.serialText.pack(side=tk.TOP, padx=5, pady=5, fill="both", expand=True)

        # self.serialText.insert("end", "Serial Monitor")

        self.ser:serial.Serial = None

        
    def connect_serial(self,event):
        # print("connecting to serial port")
        if self.ser:
            self.ser.close()
            self.ser = None
        #list ports to check
        if self.port_entry.get() in all_serial_ports():
            self.ser = serial.Serial(self.port_entry.get(), 921600)
            # self.ser.flushInput()
            # self.ser.flushOutput()
            self.flush()
            self.clear()
            self.after(100, self.interval_serial_monitor)
        else:
            self.serialText.insert("end", "Port not found\n")
            if self.ser:
                self.ser.close()
                self.ser = None
    def flush(self):
        self.ser.flushInput()
        self.ser.flushOutput()
    def clear(self):
        self.serialText.delete("0.0","end")
    def get_csi_datas(self,csi_n_sample):
        s=self.serialText.get("0.0","end")
        ss=s.strip().split("\n")

        r=[]
        count=0;
        for i in range(len(ss)-1,-1,-1):
            if count==csi_n_sample:
                break
            if ss[i].startswith("CSI_DATA"):
                row_string=ss[i]
                row_data=row_string.split(",")
                csi_data=row_data[-1].replace("[","").replace("]","").strip().split(" ")
                try:
                    csi_data=[int(x) for x in csi_data]
                except ValueError as e:
                    # print(e)
                    continue
                if len(csi_data)==128:
                    # r.append(csi_data)
                    r.insert(0,csi_data)
                    count+=1
            if count==csi_n_sample:
                break
        return r

    
    def interval_serial_monitor(self):
        if self.ser:
            try:
                # if self.ser.in_waiting > 0:
                read_bytes = self.ser.read_all().decode("utf-8")
                # print(read_bytes)
                self.serialText.insert("end", read_bytes)

            except Exception as e:
                self.serialText.insert("end", f"Error: {e}\n")
            # print("serial monitor")
        self.after(10, self.interval_serial_monitor)

class WebcamFrame(ctk.CTkFrame):
    def __init__(self, master=None):
        self.master = master
        super().__init__(
            master, 
            # border_width=2, 
            # border_color="red",
            width=200,
            height=2000
        )

        # self.webcam_label = ctk.CTkLabel(self, text="Webcam")
        # self.webcam_label.pack(side=tk.TOP, padx=5, pady=5,anchor=tk.W)


        self.save_image_var = ctk.BooleanVar(value=True)
        self.webcam_checkBox = ctk.CTkCheckBox(self, text="Save image to datasets", variable=self.save_image_var, onvalue=True, offvalue=False)
        self.webcam_checkBox.pack(side=tk.TOP, padx=5, pady=5,anchor=tk.W)

        self.video_capture = cv2.VideoCapture(0)

        self.webcam_canvas = tk.Canvas(self, width=self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH), 
                                height=self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.webcam_canvas.pack(side=tk.TOP, padx=5, pady=5, fill="both", expand=True)


        # self.webcam_canvas.create_rectangle(0, 0, 800, 600, fill="black")
        # self.webcam_canvas.create_text(400, 300, text="Webcam feed will be displayed here", fill="white")
        
        self.interval_webcam_feed()
    def interval_webcam_feed(self):
        if self.save_image_var.get()==True:
            ret, frame = self.video_capture.read()
            if ret:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(rgb_frame)
                tk_img = ImageTk.PhotoImage(image=pil_img)
                # cv2.imshow("frame", frame)
                self.webcam_canvas.delete("all")  # Clear previous frame
                self.webcam_canvas.create_image(0, 0, image=tk_img, anchor=tk.NW)
                self.webcam_canvas.image = tk_img  # Keep a reference
                # self.video_capture.release() # release the webcam
            else:
                print("No frame, recreating video capture object")
                self.video_capture = cv2.VideoCapture(0)

        self.master.after(10, self.interval_webcam_feed)




class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Datasets Collector")
        self.geometry("1280x720")

        self.collect_stop_frame = CollectStopFrame(self)
        self.collect_stop_frame.place(x=10,y=10, anchor=tk.NW)

        self.scrollable_frame = ctk.CTkScrollableFrame(self,width=1200,height=700)
        self.scrollable_frame.place(x=10, y=50, anchor=tk.NW)



        self.browsing_frame = BrowsingFrame(self.scrollable_frame)
        self.browsing_frame.pack(side=tk.TOP, padx=5, pady=5,anchor=tk.NW)

        self.map_data_frame = MapDataFrame(self.scrollable_frame)
        self.map_data_frame.pack(side=tk.TOP, padx=5, pady=5,anchor=tk.NW)

        self.csi_collection_config_frame = CSICollectionConfigFrame(self.scrollable_frame)
        self.csi_collection_config_frame.pack(side=tk.TOP, padx=5, pady=5,anchor=tk.NW)

        self.available_ports_frame = AvailablePortsFrame(self.scrollable_frame)
        self.available_ports_frame.pack(side=tk.TOP, padx=5, pady=5,anchor=tk.NW)


        self.serial_monitor1_frame = SerialMonitorFrame(self.scrollable_frame,"Port 1")
        self.serial_monitor1_frame.pack(side=tk.TOP, padx=5, pady=5,anchor=tk.NW)

        self.serial_monitor2_frame = SerialMonitorFrame(self.scrollable_frame,"Port 2")
        self.serial_monitor2_frame.pack(side=tk.TOP, padx=5, pady=5,anchor=tk.NW)

        self.webcam_frame = WebcamFrame(self.scrollable_frame)
        self.webcam_frame.pack(side=tk.TOP, padx=5, pady=5,anchor=tk.NW)
        self.interval_run()
    def interval_run(self):
        try:
            if self.collect_stop_frame.can_collect_var.get()==True:
                csi_n_sample=self.csi_collection_config_frame.csi_n_sample_var.get()

                csi_datas_1=self.serial_monitor1_frame.get_csi_datas(csi_n_sample)
                if len(csi_datas_1)!=csi_n_sample:
                    raise ValueError("len(csi_datas_1)!=csi_n_sample")
                csi_datas_2=self.serial_monitor2_frame.get_csi_datas(csi_n_sample)
                if len(csi_datas_2)!=csi_n_sample:
                    raise ValueError("len(csi_datas_2)!=csi_n_sample")
                cv2_image=None
                if self.webcam_frame.save_image_var.get()==True:
                    _,cv2_image=self.webcam_frame.video_capture.read()

                UTC_NOW = datetime.datetime.utcnow().strftime("%Y-%m-%d %H-%M-%S-%f")
                folder_path=self.browsing_frame.folder_path.get()
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                if cv2_image is not None:
                    cv2.imwrite(f"{folder_path}/{UTC_NOW}.jpg", cv2_image)
                json_dict={
                    "UTC_Time":UTC_NOW,
                    "csi_datas_1":csi_datas_1,
                    "csi_datas_2":csi_datas_2,
                    "map_data":self.map_data_frame.get_map_data(),
                    "image_url":f"{UTC_NOW}.jpg"
                }
                json.dump(json_dict, open(f"{folder_path}/{UTC_NOW}.json", "w"))


                if self.csi_collection_config_frame.clear_serial_monitor_everytime_received_var.get()==True:
                    self.serial_monitor1_frame.clear()
                    self.serial_monitor2_frame.clear()
                if self.csi_collection_config_frame.flush_everytime_received_var.get()==True:
                    self.serial_monitor1_frame.flush()
                    self.serial_monitor2_frame.flush()
        except ValueError as e:
            print(e)
        self.after(10, self.interval_run)



app = App()
app.mainloop()
