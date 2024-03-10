import datetime
import cv2
class DatasetsSaver:
    def __init__(self,folder_dir:str):
        self.folder_dir = folder_dir
        self.UTC_Time_str = ""
        self.CSI_Datas_X = []
        self.CSI_Datas_Y = []
        self.Map_Data = []
        self.Image_URL = ""
    def clear_data(self):
        self.__init__()
    def update_time(self):
        self.UTC_Time_str = datetime.datetime.utcnow().strftime("%Y-%m-%d %H-%M-%S-%f")
        self.Image_URL = f"{self.folder_dir}/{self.UTC_Time_str}.jpg"
    def is_saving_ready(self):
        if self.UTC_Time_str=="" or len(self.CSI_Datas_X) == 0 or len(self.CSI_Datas_Y) == 0 or len(self.Map_Data) == 0 or self.Image_URL == "":
            return False
    def save_json():
        pass
    def save_img():
        pass
    

datasets_saver = DatasetsSaver()