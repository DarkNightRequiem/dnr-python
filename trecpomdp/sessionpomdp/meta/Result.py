from sessionpomdp.meta.Element import Element
from sessionpomdp.util.rlvMap import rlvDict


class Result(Element):
    def __init__(self, rank, url, webID, title, snippet, topicID):
        self.rank = rank
        self.url = url
        self.webID = webID
        self.title = title
        self.snippet = snippet
        # 计算result和topic的切合度 R:relevant True  NR: Non-Relevant False
        self.relevance = self.calRelevance(self.webID, topicID)

    def printContent(self):
        print("\t\trank: ", self.rank, "\twebID: ", self.webID, "\trelevance: ", self.relevance)

    def calRelevance(self, webID, topicID):
        key = topicID + "*" + webID
        # 在12和13年的overview中 =1是relevant
        if key in rlvDict.keys():
            if rlvDict[key] >= 1:
                return True
            else:
                return False
        else:
            print("missing judgement: ", webID, "topid ID: ", topicID)
            # 应为已经观察过一次输出结果，发现是官方没有的都是true.所以return true
            return True
