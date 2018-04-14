from util.Element import Element


class Click(Element):
    def __init__(self, rank, starttime, endtime):
        self.rank = rank
        self.starttime = starttime
        self.endtime = endtime
        # TODO: 计算时差并分类（是否SAT）

    def printContent(self):
        print("\tClick <rank=",self.rank,"start=",self.starttime,"end=",self.endtime,">")
