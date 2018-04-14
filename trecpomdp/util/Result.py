from util.Element import Element


class Result(Element):
    def __init__(self, rank, url, webID, title, snippet):
        self.rank = rank
        self.url = url
        self.webID = webID
        self.title = title
        self.snippet = snippet

    def printContent(self):
        print("Result <rank=",self.rank," webID=",self.webID)
