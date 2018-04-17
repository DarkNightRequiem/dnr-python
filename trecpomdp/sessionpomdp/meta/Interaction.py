from sessionpomdp.meta.Element import Element


class Interaction(Element):
    def __init__(self, it):
        self.year=it["year"]
        self.topicID=it["topicID"]
        self.topic= it["topic"]
        self.query = it["query"]
        self.results = it["results"]
        self.clicked = it["clicked"]
        self.isSessionEnd=it["isSessionEnd"]

    def printContent(self):
        print("topicID:",self.topicID,
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
