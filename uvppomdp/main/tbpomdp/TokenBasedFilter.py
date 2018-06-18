# --------------------------------------------
# @File     : TokenBasedFilter.py
# @Time     : 2018/6/18 16:13
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : 
# --------------------------------------------
import os
import json
from util.ConfigReader import config_reader
from util.ColorfulLogger import logger


class TokenBasedFilter:

    def __init__(self,input_dir,output_dir,api_path):
        self.input_dir=input_dir
        self.output_dir=output_dir
        self.api_path=api_path

        if not os.path.exists(output_dir):
            os.mkdir(self.output_dir)

        if not os.path.exists(input_dir):
            logger.error(self.__class__, "No Merged Results Detected!")

        self.api=None

    def filter(self):
        file_names=os.listdir(self.input_dir)
        for filename in file_names:
            with open(self.input_dir+"/"+filename,"r") as file:
                # 获取Token列表
                data=json.load(file)
                tokens=data["tokens"]

                print("hh")
            file.close()

    def builtApiSet(self):
        # TODO: 实现
        with open(self.api_path) as api_file:
            pass
        api_file.close()


if __name__ == '__main__':
    # 获取配置信息
    input_dir = config_reader.tb_tokenbasedmerger_output_dir
    output_dir = config_reader.tb_tokenbasedfilter_ouput_dir
    api_path=config_reader.uwp_api_path

    # 建立标识符集合

    # 过滤
    tbfilter=TokenBasedFilter(input_dir,output_dir,api_path)
    tbfilter.filter()

