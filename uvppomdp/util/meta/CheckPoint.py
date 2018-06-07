class CheckPoint:
    def __init__(self):
        self.filename=None

        self.from_id=None
        self.from_date=None

        self.to_id=None
        self.to_date=None

        # 时间点记录器
        self.record=None

    def isborder(self):
        """
        判断否是学号边界比较文件
        """
        if self.from_id != self.to_id:
            return True
        else:
            return False

    def update(self):
        """
        更新时间点记录器
        :return:
        """
        if self.record is None:
            # 还未设置过时间点记录
            self.record=[self.from_date, self.to_date]

        elif self.record[1]==self.from_id:
            # 上一个文件也是无变化文件
            self.record[1]=self.to_id

        elif self.record[1]!=self.from_id:
            # 上一个文件是有变化文件
            self.record = [self.from_date, self.to_date]

    def reset(self):
        """
        重置时间点记录器
        """
        self.filename=None

        self.from_id=None
        self.from_date=None

        self.to_id=None
        self.to_date=None

        self.record=None

    def setinfo(self,filename):
        """
        设置文件信息
        :param filename:
        :return:
        """
        from_to=filename.split("=")

        self.from_id=from_to[0].split("-",1)[0]
        self.from_date=from_to[0].split("-",1)[1]

        self.to_id=from_to[1].replace(".json","").split("-",1)[0]
        self.to_date=from_to[1].replace(".json","").split("-",1)[1]

