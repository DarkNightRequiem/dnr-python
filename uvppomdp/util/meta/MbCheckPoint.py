class MbCheckPoint:
    def __init__(self):
        # 当前文件信息
        self.filename = None

        self.is_empty = False
        self.is_border = False

        self.from_id = None
        self.from_date = None

        self.to_id = None
        self.to_date = None

        # 全局时间点记录器
        self.record = None
        # 全局数据缓冲区
        self.buffer = None

    def update(self):
        """
        更新时间点记录器
        """
        if self.record is None:
            # 还未设置过时间点记录
            self.record = [self.from_date, self.to_date]
            buffer = self.release_buffer()
            return buffer

        elif "0" == self.record[0]:
            # 最新记录是该学生的首次提交
            self.record = [self.from_date, self.to_date]

        elif (not self.is_empty) and (self.from_date == self.record[1]):
            # 当前文件有记录变化
            self.record[1] = self.to_date
            buffer =self.release_buffer()
            return buffer

        elif self.is_empty:
            # 当前和其之前的文件都没有记录变化
            self.record[1] = self.to_date

        else:
            # 释放现有缓冲区并重新时间记录
            buffer = self.release_buffer()
            self.record=[self.from_date, self.to_date]
            return buffer

        return None

    def release_buffer(self):
        """
        将当前缓冲区中的文件清空并返回内容
        :return: 上次清空后至此次调用缓冲区所积累的内容
        """
        bf = self.buffer
        self.buffer = None
        return bf

    def reset(self):
        """
        重置时间点记录器
        """
        self.filename = None

        self.from_id = None
        self.from_date = None

        self.to_id = None
        self.to_date = None

        self.record = None
        self.buffer = None

    def setinfo(self, filename, data):
        """
        设置文件信息
        """
        from_to = filename.split("=")
        self.filename = filename

        self.from_id = from_to[0].split("-", 1)[0]
        self.from_date = from_to[0].split("-", 1)[1]

        self.to_id = from_to[1].replace(".json", "").split("-", 1)[0]
        self.to_date = from_to[1].replace(".json", "").split("-", 1)[1]

        self.is_empty = self.isempty(data)
        self.is_border = self.isborder()

        if self.buffer is None:
            self.buffer = []
        if not self.is_empty:
            self.buffer.append(data)

    def isempty(self, data):
        """
        判断文件是否记录空信息
        :return:
        """
        flag = True

        for key in data.keys():
            if key not in ['from', 'to']:
                if data[key].__len__() > 0:
                    flag = False

        return flag

    def isborder(self):
        """
        判断否是学号边界比较文件
        """
        if self.from_date == "0":
            return True
        else:
            return False
