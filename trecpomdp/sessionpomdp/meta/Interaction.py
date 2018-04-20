from sessionpomdp.meta.Element import Element
from sessionpomdp.util.explMap import explDict12, explDict13
from sessionpomdp.meta.Click import Click


class Interaction(Element):
    def __init__(self, it):
        self.year = it["year"]
        self.topicID = it["topicID"]
        self.topic = it["topic"]
        self.query = it["query"]
        self.results = it["results"]
        self.clicked = it["clicked"]
        self.isSessionEnd = it["isSessionEnd"]
        self.position = it["position"]
        self.sessionID = it["sessionID"]

        # 计算 exploration dimension True: exploration False: exploitation
        self.expl = self.calExplo(self.sessionID, self.position, self.year,self.query)
        # clicked 中的SAT的个数和非SAT的个数
        self.clickedSAT,self.clickedNonSAT=self.countSAT(self.clicked)

    def calExplo(self, sessionID, position, year,query):
        k = str(position) + "*" + query
        if year == 2012:
            if explDict12[sessionID][k] == "R":
                return True
            else:
                return False
        elif year == 2013:
            if explDict13[sessionID][k] == "R":
                return True
            else:
                return False

    def countSAT(self, clkd):
        """
        计算此次interaction的点击中SAT和非SAT的个数
        """
        cSAT=0
        cNoSAT=0
        if clkd is None:
            return 0,0
        for clk in clkd:
            if clk.isSAT:
                cSAT+=1
            else:
                cNoSAT+=1
        return cSAT,cNoSAT

    def printContent(self):
        print("topicID:", self.topicID, "\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\texpl: ", self.expl,
              "\nquery: ", self.query)

        if self.isSessionEnd:
            print("End of a session")
            print("=======================================================================\n")
            return
        print("results:")
        for res in self.results:
            res.printContent()

        # if (self.clicked is None) or (self.clicked.__len__()<=0):
        #     return
        if self.clicked is None:
            return
        print("Clicked:")
        for clk in self.clicked:
            clk.printContent()
