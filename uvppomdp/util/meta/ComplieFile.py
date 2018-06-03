import time


class CompileFile:
    def __init__(self, filename, contents):
        # TODO: 修改完善
        # 文件名
        self.filename = filename

        # 对应学号和时间信息
        self.id, \
        self.date, \
        self.timestamp = self.get_info(self.filename)

        # 日志内文件字典
        # key: 日志内的文件全路径，如 test.zip/app.xaml
        # value: 对应的文件内容
        self.contents = contents

    def get_info(self, filename):
        """
        解析文件名所含有的信息
        """
        # 获取学号和日期字符串
        stuid, suffix = filename.split('-', 1)

        # 解析日期信息
        date = time.strptime(suffix.replace(".zip", ""), "%Y-%m-%d-%H-%M-%S")
        timestamp = time.mktime(date)

        return stuid, date, timestamp

    def get_content(self, path):
        """
        根据压缩文件内的路径获取对应文件内容
        """
        if self.has_path(path):
            return self.contents[path]
        else:
            return None

    def has_path(self, path):
        """
        判断当前编译日志文件是否含有某个路径
        """
        if path in self.contents.keys():
            return True
        else:
            return False
