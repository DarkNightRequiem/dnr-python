from sessionpomdp.meta.Element import Element


class Result(Element):
    def __init__(self, rank, url, webID, title, snippet):
        self.rank = rank
        self.url = url
        self.webID = webID
        self.title = title
        self.snippet = snippet
        # TODO: 计算relevance: R:relevant NR: Non-Relevant

    def printContent(self):
        print("\t\trank: ",self.rank, "\twebID: ",self.webID,"\trelevance: ","ToCal")
