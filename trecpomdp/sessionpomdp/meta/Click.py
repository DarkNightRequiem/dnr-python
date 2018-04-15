from sessionpomdp.meta.Element import Element


class Click(Element):
    def __init__(self, rank, starttime, endtime):
        self.rank = rank
        self.starttime = starttime
        self.endtime = endtime
        # TODO: 计算驻留时间 residence 并分类（是否SAT）(>30s)

    def printContent(self):
        print("\t\trank: ", self.rank, "\tresidence: ", "ToCal", "\tSAT: ", "ToCal")
