# --------------------------------------------
# @File     : SearchSessionExtractor.py
# @Time     : 2018/7/7 21:26
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : 对缩减后的日志提取只和serp有关的部分
# --------------------------------------------
import os, shutil
import json
import time
import chardet

from util.ColorfulLogger import logger
from util.ConfigReader import config_reader


class SearchSessionExtractor:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

        if not os.path.exists(output_dir):
            os.mkdir(self.output_dir)

        if not os.path.exists(input_dir):
            logger.error(self.__class__, "No Shrunken Log Detected!")

    def extract(self):
        file_names=os.listdir(self.input_dir)
        if file_names.__len__()<=0:return

        for name in file_names:
            # 首先获取一个文件中的所有serp
            file= open(self.input_dir+"/"+name,"r")

            session_list=json.loads(file.read())
            if session_list.__len__()<=0:
                file.close()
                continue



            # TODO:实现
            file.close()
            # 然后根据serp来筛选剩下的页面
            pass


        pass


if __name__ == '__main__':
    input_dir = config_reader.tb_logshrinker_output_dir
    output_dir = config_reader.tb_searchsessionextractor_output_dir

    extractor = SearchSessionExtractor(input_dir, output_dir)
    extractor.extract()
