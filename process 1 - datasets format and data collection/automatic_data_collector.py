import serial
import json
import time
import datetime
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from adc_serial_monitor import *
from adc_datasets_saver import *
# 1 = ESP pair 1
# 2 = ESP pair 2

def save_json(url,UTC_Time,CSI_Datas_X,CSI_Datas_Y,Map_Data,Image_URL):
    with open(f"{url}.json", "w") as f:
        json.dump({
            "UTC_Time":UTC_Time,
            "CSI_Datas_X":CSI_Datas_X,
            "CSI_Datas_Y":CSI_Datas_Y,
            "Map_Data":Map_Data,
            "Image_URL":Image_URL}, f)
def save_cam_img(url):
    pass



#user input part
start=False
save_img=False
while start==False:
    PORT_1 = input("Enter the port for ESP RX pair 1 : ")
    PORT_2 = input("Enter the port for ESP RX pair 2 : ")
    map_data:list[list[int]] = json.loads(input("Enter the map data to label (4x4 array): "))
    save_img=input("Do you want to save the image? (y/n): ").lower()
    if save_img=="y":
        save_img=True
    else:
        save_img=False
    folder_dir = input("Enter the folder directory to save the file in : ")
    print(f"The json file will be saved in this format : {folder_dir}/{{UTC_Time}}.json")
    print(f"The image file will be saved in this format : {folder_dir}/{{UTC_Time}}.jpg")
    start=input("Start the program? (y/n): ").lower()
    if start=="y":
        start=True
    else:
        start=False

#serial port setup
ser_1 = serial.Serial(PORT_1, 921600)
ser_2 = serial.Serial(PORT_2, 921600)

#start writing datasets
while True:
    ser_1.flushInput()
    ser_1.flushOutput()
    ser_2.flushInput()
    ser_2.flushOutput()

    set_of_data_1 = []
    set_of_data_2 = []

    while len(set_of_data_1)<20 and len(set_of_data_2)<20:
        try:
            line_1 = ser_1.readline().decode("utf-8").strip()
            line_2 = ser_2.readline().decode("utf-8").strip()
            if line_1.startswith("CSI_DATA") and line_2.startswith("CSI_DATA"):
                csi_data_1_str= line_1.split(",")[-1].replace("[","").replace("]","")
                csi_data_2_str= line_2.split(",")[-1].replace("[","").replace("]","")
                csi_data_1 = list(map(int, csi_data_1_str.split(" ")))
                csi_data_2 = list(map(int, csi_data_2_str.split(" ")))
        except UnicodeDecodeError as e:
            print(e)
            continue

    time.sleep(1)