from sessionpomdp.meta.Element import Element
from sessionpomdp.util.explMap import explDict12,explDict13

class Interaction(Element):
    def __init__(self, it):
        self.year=it["year"]
        self.topicID=it["topicID"]
        self.topic= it["topic"]
        self.query = it["query"]
        self.results = it["results"]
        self.clicked = it["clicked"]
        self.isSessionEnd=it["isSessionEnd"]
        self.position=it["position"]
        self.sessionID=it["sessionID"]

    def getExplo(self,sessionID,position):
        # TODO: 实现判断
        pass

    def printContent(self):
        print("topicID:",self.topicID,"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tposition: ",self.position,
              "\nquery: ",self.query)

        if self.isSessionEnd :
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
