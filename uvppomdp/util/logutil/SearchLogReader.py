import os
import platform
import yaml
from util.logutil.BasicUtil import BasicUtil


class SearchLogReader(BasicUtil):
    def __init__(self):
        BasicUtil.__init__(self)

        # 搜索日志存放目录
        self.dir=self.cfg.get("search.log")["dir"]

        # 搜索日志文件列表
        self.files=os.listdir(self.dir)


# if __name__ == '__main__':
#     clr=BrowseLogReader()
#     print("dd")
