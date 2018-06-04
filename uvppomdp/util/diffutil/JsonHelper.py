import json
from util.BasicUtil import BasicUtil


class JsonHelper(BasicUtil):
    def __init__(self):
        BasicUtil.__init__(self)

        # 垃圾内容
        self.junks=['\r','\n','\r\n']




json_helper=JsonHelper()