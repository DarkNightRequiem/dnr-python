# --------------------------------------------
# @File     : MediaPlayerExtractor.py
# @Time     : 2018/7/5 16:29
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : 提取出任务为MediaPlayer的json文件
# --------------------------------------------
import os
import time
import json
import re
import zipfile

from util.ColorfulLogger import logger
from util.ConfigReader import config_reader


class MediaPlayerExtractor:
    def __init__(self, input_dir, output_dir, uploads_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.uploads_dir = uploads_dir

        if not os.path.exists(output_dir):
            os.mkdir(self.output_dir)

        if not os.path.exists(input_dir):
            logger.error(self.__class__, "No Merged Results Detected!")

        self.project_name_dict = self.get_project_name_dict()

    def extract(self):
        file_names = os.listdir(self.input_dir)
        if file_names.__len__() <= 0: return

        for name in file_names:
            date = time.strptime(name.split("-", 1)[1].replace(".json", ""), "%Y-%m-%d-%H-%M-%S")
            if 3 < date.tm_mon < 5:
                if (name in self.project_name_dict.keys()) and \
                        (re.search(r"[Mm][Ee][Dd][Ii][Aa][Pp][Ll][Aa][Yy][Ee][Rr]",
                                  self.project_name_dict[name]) is not None):
                    # 是播放器课程
                    with open(self.input_dir + "/" + name, "r") as file:
                        data = json.load(file)
                        data["project_name"]="MediaPlayer"
                        self.write_as_json(data,name)

                    file.close()

    def get_project_name_dict(self):
        """
        从原始的上传文件中提取工程名
        """
        project_name_dict = {}
        file_names = os.listdir(self.uploads_dir)

        for name in file_names:
            try:
                zip = zipfile.ZipFile(self.uploads_dir + "/" + name, "r")
                if zip.filelist.__len__() <= 0: continue
                project_name = zip.filelist[0].filename.split("/")[0]
                project_name_dict[name.replace(".zip",".json")] = project_name
            except zipfile.BadZipFile:
                continue

        return project_name_dict

    def write_as_json(self,json_recognizable,filename):
        """
         写入json文件
        """
        json_content = json.dumps(json_recognizable, indent=4)
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)
        with open(
                os.path.join(self.output_dir, filename),
                "w",encoding="utf-8"
        ) as file:
            file.write(json_content)
        file.close()


if __name__ == '__main__':
    input_dir = config_reader.tb_tokenbasedmerger_output_dir
    output_dir = config_reader.tb_tokenbasedextractor_mediaplayer_output_dir
    uploads_dir = config_reader.compile_logs_uploads_dir

    extractor = MediaPlayerExtractor(input_dir, output_dir, uploads_dir)
    extractor.extract()
