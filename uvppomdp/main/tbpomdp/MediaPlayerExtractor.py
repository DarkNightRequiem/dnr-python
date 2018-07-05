# --------------------------------------------
# @File     : MediaPlayerExtractor.py
# @Time     : 2018/7/5 16:29
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : 
# --------------------------------------------
import os
import time
import json
from util.ColorfulLogger import logger
from util.ConfigReader import config_reader


class MediaPlayerExtractor:
    def __init__(self,input_dir,output_dir,uploads_dir):
        self.input_dir=input_dir
        self.output_dir=output_dir
        self.uploads_dir=uploads_dir

        if not os.path.exists(output_dir):
            os.mkdir(self.output_dir)

        if not os.path.exists(input_dir):
            logger.error(self.__class__, "No Merged Results Detected!")

        self.project_name_dict=

    def extract(self):
        file_names=os.listdir(self.input_dir)
        if file_names.__len__()<=0:return

        for name in file_names:
            date=time.strptime(name.split("-",1)[1].replace(".json",""),"%Y-%m-%d-%H-%M-%S")
            if(date.tm_mon>3 and date.tm_mon<5):



            print("cc")
            pass


    def get_project_name_dict(self):
        project_name_dict={}

        file_names=os.listdir(self.uploads_dir)
        for name in file_names:
            

        pass


if __name__=='__main__':
    input_dir=config_reader.tb_tokenbasedmerger_output_dir
    output_dir=config_reader.tb_tokenbasedextractor_mediapalyer_output_dir
    uploads_dir=config_reader.compile_logs_uploads_dir

    extractor=MediaPlayerExtractor(input_dir,output_dir,uploads_dir)
    extractor.extract()