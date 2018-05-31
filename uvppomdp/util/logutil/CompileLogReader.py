import os
import platform
import yaml
from util.logutil.BasicUtil import BasicUtil


class ComplieLogReader(BasicUtil):
    def __init__(self):
        BasicUtil.__init__(self)

        # 编译日志存放目录
        self.dir=self.cfg.get("compile.log")["dir"]

        # 编译日志文件列表
        self.files=os.listdir(self.dir)


# if __name__ == '__main__':
#     clr=ComplieLogReader()
#     print("dd")
