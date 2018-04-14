from util.Element import Element


class Interaction(Element):
    def __init__(self, it):
        self.topicID=it["topicID"]
        self.topic= it["topic"]
        self.query = it["query"]
        self.results = it["results"]
        self.clicked = it["clicked"]

    def printContent(self):
        print("Interaction <topicID=",self.topicID," query=",self.query)
