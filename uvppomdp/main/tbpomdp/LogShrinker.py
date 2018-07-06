# --------------------------------------------
# @File     : LogShrinker.py
# @Time     : 2018/7/6 19:58
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : 将用户的搜索日志缩减至MediaPlayer任务期间
# --------------------------------------------
import os, shutil
import json
import time
import chardet

from util.ColorfulLogger import logger
from util.ConfigReader import config_reader


class LogShrinker:
    def __init__(self, search_logs_dir, output_dir):
        self.search_logs_dir = search_logs_dir
        self.output_dir = output_dir

        if not os.path.exists(output_dir):
            os.mkdir(self.output_dir)

        if not os.path.exists(search_logs_dir):
            logger.error(self.__class__, "No Search Log Detected!")

    def shrink(self):
        file_names = os.listdir(self.search_logs_dir)
        if file_names.__len__() <= 0: return

        for name in file_names:
            with open(search_logs_dir + "/" + name, "rb")as file:
                # 查看文件编码
                data=file.read()
                # encode = (chardet.detect(data))["encoding"] \
                #     if (chardet.detect(data))["encoding"] is not None \
                #     else "utf-8"

                session_list = json.loads(data)
                for session in session_list:
                    # 隐式session删除
                    if session["mergedAction"]=="latentSession":
                        session_list.remove(session)
                        continue

                    merged_actions=session["mergedActions"]
                    for action in merged_actions:
                        timestamp=action["timestamp"]
                        time_tuple=time.gmtime(timestamp/1000)

                        # 不在Media课程范内的删除
                        if 3<time_tuple.tm_mon<5:
                            merged_actions.remove(action)

                        print("cc")

                # TODO:写入新的文件

            file.close()
        pass


if __name__ == '__main__':
    search_logs_dir = config_reader.search_logs_dir
    output_dir = config_reader.tb_tokenbasedlogshrinker_output_dir

    shrinker = LogShrinker(search_logs_dir, output_dir)
    shrinker.shrink()
