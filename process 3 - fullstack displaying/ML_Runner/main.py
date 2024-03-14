import tkinter as tk
import customtkinter as ctk
import numpy as np
import sys
import serial
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("Importing tensorflow")
import tensorflow as tf
print("Importing tensorflow.keras")
from tensorflow.keras import layers, models


class CSILocalizer:
    def __init__(self, model_path,model_weight_path):
        self.model = models.load_model(model_path)
        self.model.load_weights(model_weight_path)
        print(self.model.summary())
    def get_map_data(self,Input):
        if Input.shape!=(2,20,128):
            raise ValueError("Input shape should be (2,20,128)")
        return np.round(self.model.predict(np.array([Input]))[0])

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


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


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CSI Localizer")
        self.geometry("1280x720")

        self.csi_localizer=CSILocalizer("model copy 2.h5","model_weights copy 2.h5")

        self.csi_collection_config_frame = CSICollectionConfigFrame(self)
        self.csi_collection_config_frame.pack(side=tk.TOP, padx=5, pady=5, anchor=tk.NW)

        self.available_ports_frame = AvailablePortsFrame(self)
        self.available_ports_frame.pack(side=tk.TOP, padx=5,pady=5,anchor=tk.W)

        self.serial_monitor1_frame = SerialMonitorFrame(self,placeholder_port="Port 1")
        self.serial_monitor1_frame.pack(side=tk.TOP, padx=5,pady=5,anchor=tk.W)

        self.serial_monitor2_frame = SerialMonitorFrame(self,placeholder_port="Port 2")
        self.serial_monitor2_frame.pack(side=tk.TOP, padx=5,pady=5,anchor=tk.W)


        self.interval_run()
    def interval_run(self):
        try:
            csi_n_sample=self.csi_collection_config_frame.csi_n_sample_var.get()
            csi_datas1=self.serial_monitor1_frame.get_csi_datas(csi_n_sample)
            if len(csi_datas1)!=csi_n_sample:
                raise ValueError("len(csi_datas1)!=csi_n_sample")
            csi_datas2=self.serial_monitor2_frame.get_csi_datas(csi_n_sample)
            if len(csi_datas2)!=csi_n_sample:
                raise ValueError("len(csi_datas2)!=csi_n_sample")
            
            csi_datas=np.array([csi_datas1,csi_datas2])
            map_data=self.csi_localizer.get_map_data(csi_datas)
            print(map_data)

            if self.csi_collection_config_frame.flush_everytime_received_var.get():
                self.serial_monitor1_frame.flush()
                self.serial_monitor2_frame.flush()
            if self.csi_collection_config_frame.clear_serial_monitor_everytime_received_var.get():
                self.serial_monitor1_frame.clear()
                self.serial_monitor2_frame.clear()

            
        except ValueError as e:
            # print(e)
            if str(e)!="len(csi_datas1)!=csi_n_sample" and str(e)!="len(csi_datas2)!=csi_n_sample":
                print(e)
        self.after(10, self.interval_run)

app=App()
app.mainloop()