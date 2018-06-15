# --------------------------------------------
# @File     : SearchLogReader.py
# @Time     : 2018/6/7 21:14
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     :
# --------------------------------------------
import os
from util.ConfigReader import ConfigReader


class SearchLogReader(ConfigReader):
    def __init__(self):
        ConfigReader.__init__(self)

        # 搜索日志存放目录
        self.dir=self.cfg.get("search.log")["dir"]

        # 搜索日志文件列表
        self.files=os.listdir(self.dir)


# 利用模块的导入机制实现单例模式
srchl_reader=SearchLogReader()
