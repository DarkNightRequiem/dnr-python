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

        # 上一个文件的信息
        self.pre_empty= False
        self.pre_id=None

        # 全局时间点记录器
        self.record = None
        # 全局数据缓冲区
        self.buffer = None

    def update(self):
        """
        更新时间点记录器
        """
        # 是否需要释放缓冲区
        need_pop=False

        if self.is_border or "0" == self.record[0]:
            # 新的学生 或 上次空记录时间是新的学生
            self.record = [self.from_date, self.to_date]
            self.pre_id=self.to_id
            need_pop = True if not self.is_empty else False

        elif not self.is_empty:
            # 当前文件有记录变化
            need_pop = True

            if self.pre_empty:
                # 上个文件无记录变化
                self.record[1]=self.to_date
            elif not self.pre_empty:
                # 上个文件有记录变化
                self.record=[self.from_date, self.to_date]

        elif self.is_empty:
            # 当前文件无记录变化
            need_pop = False

            if self.pre_empty:
                # 上个文件无记录变化
                self.record[1] = self.to_date
            elif not self.pre_empty:
                # 上个文件有记录变化
                self.record = [self.from_date, self.to_date]

        self.pre_empty=self.is_empty
        return need_pop

    def pop_data(self):
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

        self.pre_empty=False
        self.pre_id=None

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
                    for subkey in data[key].keys():
                        if data[key][subkey].__len__()>0:
                            flag=False

        return flag

    def isborder(self):
        """
        判断否是学号边界比较文件
        """
        if self.from_date == "0":
            return True
        else:
            return False
