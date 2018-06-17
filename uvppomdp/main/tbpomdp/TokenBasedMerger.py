# --------------------------------------------
# @File     : TokenBasedMerger.py
# @Time     : 2018/6/17 21:04
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : TokenBasedMerger
# --------------------------------------------
import os
from util.ColorfulLogger import logger
from util.ConfigReader import config_reader


class TokenBasedMerger:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

        if not os.path.exists(output_dir):
            os.mkdir(self.output_dir)

        if not os.path.exists(input_dir):
            logger.error(self.__class__, "No Preprocessed Results Detected!")

        # 学生学号列表
        self.stuid_list=[]

    def merge(self):
        file_names=os.listdir(self.output_dir)

        for i in range(1,file_names.__len__()-1):
            with open(self.input_dir+"/"+file_names[i],"r") as current_file:
                with open(self.input_dir+"/"+file_names[i+1],"r") as next_file:
                    # TODO:实现merge

                    pass
                next_file.close()
            current_file.close()


if __name__ == '__main__':
    # 获取配置信息
    input_dir = config_reader.tb_tokenbasedpreprocessor_output_dir
    output_dir = config_reader.tb_tokenbasedmerger_output_dir

    # 进行合并
    merger = TokenBasedMerger(input_dir, output_dir)
    merger.merge()
