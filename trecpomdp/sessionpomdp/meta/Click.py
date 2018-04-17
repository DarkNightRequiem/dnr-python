from sessionpomdp.meta.Element import Element
import datetime as dt


class Click(Element):
    def __init__(self, rank, starttime, endtime):
        self.rank = rank
        self.starttime = starttime
        self.endtime = endtime
        if ":" in self.starttime:
            st = dt.datetime.strptime(starttime[0:-7], "%H:%M:%S")
            et = dt.datetime.strptime(endtime[0:-7], "%H:%M:%S")
            du=(et-st).total_seconds()
        else:
            st = float(starttime)
            et = float(endtime)
            du = et-st
        if du >30:
            self.isSAT=True
        else:
            self.isSAT=False

    def printContent(self):
        print("\t\trank: ", self.rank, "\tresidence: ", "ToCal", "\tSAT: ", self.isSAT)
