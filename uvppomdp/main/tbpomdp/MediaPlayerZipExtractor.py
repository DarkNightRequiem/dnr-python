# --------------------------------------------
# @File     : MediaPlayerZipExtractor.py
# @Time     : 2018/7/6 16:47
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : 抽取MediaPlayer任务的上传代码文件
# --------------------------------------------
import os,shutil

from util.ColorfulLogger import logger
from util.ConfigReader import config_reader


class MediaPlayerZipExtractor:
    def __init__(self,  input_dir, output_dir,uploads_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.uploads_dir=uploads_dir

        if not os.path.exists(output_dir):
            os.mkdir(self.output_dir)

        if not os.path.exists(input_dir):
            logger.error(self.__class__, "No Extracted MediaPlayer Json File Detected!")

    def extract(self):
        file_names = os.listdir(self.input_dir)
        if file_names.__len__() <= 0: return

        for name in file_names:
            src_path=self.uploads_dir+"/"+name.replace(".json",".zip")
            dst_path=self.output_dir+"/"+name.replace(".json",".zip")
            if os.path.exists(src_path):
                shutil.copyfile(src_path,dst_path)


if __name__ == '__main__':
    input_dir = config_reader.tb_mediaplayer_extractor_output_dir
    output_dir = config_reader.tb_mediaplayer_zipextractor__output_dir
    uploads_dir=config_reader.compile_logs_uploads_dir

    extractor = MediaPlayerZipExtractor(input_dir, output_dir,uploads_dir)
    extractor.extract()
