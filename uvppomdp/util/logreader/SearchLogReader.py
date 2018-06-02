import os
from util.BasicUtil import BasicUtil


class SearchLogReader(BasicUtil):
    def __init__(self):
        BasicUtil.__init__(self)

        # 搜索日志存放目录
        self.dir=self.cfg.get("search.log")["dir"]

        # 搜索日志文件列表
        self.files=os.listdir(self.dir)


# 利用模块的导入机制实现单例模式
srchl_reader=SearchLogReader()
