# index for purely add action
IDX_ADD = 0
# index for purely remove action
IDX_RMV = 1
# index for purely keeping action
IDX_KEP = 2
# index for add and  remove action
IDX_APR = 3
# index for user click action
IDX_CLK = 4


class Action:
    def __init__(self, aList, rList, kList):
        """
        总共有四种domain-level的动作 A R K AR（这里不用考虑message-level的动作）
        :param aList: 添加的词的列表
        :param rList: 减少的词的列表
        :param kList: 不变的词的列表
        """
        # Add
        self.aList = aList
        # Remove
        self.rList = rList
        # Keep
        self.kList = kList
        # 各种动作是否存在的标志 False为不存在
        self.af = self.rf = self.kf = self.arf = False
        if aList.__len__() > 0 and rList.__len__() > 0:
            self.arf = True
        if aList.__len__() > 0 >= rList.__len__():
            self.af = True
        if rList.__len__() > 0 >= aList.__len__():
            self.rf = True
        # if kList.__len__() > 0>=rList.__len__()>=aList.__len__():
        if kList.__len__() > 0:
            self.kf = True
