import datetime as dt
import xml.dom.minidom as minidom

from sessionpomdp.meta.Click import Click
from sessionpomdp.meta.Interaction import Interaction

from sessionpomdp.meta.Result import Result


# () 元组
# [] 列表
# {} 字典
# 使用dom解析xml文件
class TrecDomParser:
    def __init__(self, path, year):
        # 日志所属的年份,不同年份对应的处理方式稍有不同
        self.year = year
        # 要解析的文件路径
        self.path = path
        # 文件中的DomTree
        self.domTree = minidom.parse(path)
        # 文件中的所有的dom元素
        self.collection = self.domTree.documentElement
        # 所有的<session>
        self.sessions = self.collection.getElementsByTagName("session")
        #
        self.topicDict = []
        #
        self.longSessions = []

    @staticmethod
    def concat(s1=list, s2=list):
        """
        连接两个sessions
        :return: 连接后的sessions
        """
        s1.extend(s2)
        return s1

    @staticmethod
    def getTrainSamples(sessions,year):
        """
        获取训练样本，每个session的current query作为一个没有结果和点击的interaction
        :param sessions: 样本源
        :return:
        """
        itList = []
        for session in sessions:
            topicID = session.getElementsByTagName("topic")[0].getAttribute("num")
            topic = session.getElementsByTagName("topic")[0].getElementsByTagName("desc")[0].childNodes[0].data

            c = session.getElementsByTagName("interaction")
            for ci in c:
                tempDict = {}
                tempDict["topicID"] = topicID
                tempDict["topic"] = topic
                tempDict["year"]=year
                q=str(ci.getElementsByTagName("query")[0].childNodes[0].data)
                tempDict["query"] = q

                # results列表
                ress = []
                results = ci.getElementsByTagName("results")[0].getElementsByTagName("result")
                for i in range(results.__len__()):
                    # 文档的rank
                    rank = results[i].getAttribute("rank")
                    # 文档的url
                    url = results[i].getElementsByTagName("url")[0].childNodes[0].data
                    # 文档的clueweb id
                    webID = results[i].childNodes[3].childNodes[0].data

                    title = results[i].getElementsByTagName("title")[0].childNodes
                    if title.__len__() == 0:
                        title = None
                    else:
                        title = results[i].getElementsByTagName("title")[0].childNodes[0].data

                    snippet = results[i].getElementsByTagName("snippet")[0].childNodes
                    if snippet.__len__() == 0:
                        snippet = None
                    else:
                        snippet = results[i].getElementsByTagName("snippet")[0].childNodes[0].data
                    res = Result(rank, url, webID, title, snippet,topicID)
                    ress.append(res)
                tempDict["results"] = ress

                # clicked列表
                clkd = None
                clcs = ci.getElementsByTagName("clicked")
                if clcs.__len__() != 0:
                    clkd = []
                    clcs = ci.getElementsByTagName("clicked")[0].getElementsByTagName("click")
                    for i in range(clcs.__len__()):
                        clk = Click(clcs[i].getElementsByTagName("rank")[0].childNodes[0].data,
                                    clcs[i].getAttribute("starttime"),
                                    clcs[i].getAttribute("endtime")
                                    )
                        clkd.append(clk)
                if clcs.__len__()==0:
                    clkd=None
                tempDict["clicked"] = clkd
                tempDict["isSessionEnd"]=False
                interaction = Interaction(tempDict)
                itList.append(interaction)

            # currentquery 一个session中的最后一个查询
            cq = session.getElementsByTagName("currentquery")[0].getElementsByTagName("query")[0].childNodes[0].data
            cqDict = {}
            cqDict["year"]=year
            cqDict["topicID"] = topicID
            cqDict["topic"] = topic
            cqDict["query"] = cq
            cqDict["results"] = None
            cqDict["clicked"] = None
            cqDict["isSessionEnd"]=True
            endInteraction = Interaction(cqDict)
            itList.append(endInteraction)

        return itList

    def getLongSessions(self, length):
        """
        获取query数>= length 的sessions
        :param length: session length
        :return:
        """
        for session in self.sessions:
            interactionNum = list(session.getElementsByTagName("interaction")).__len__()
            curQuery = list(session.getElementsByTagName("currentquery")).__len__()
            if (interactionNum + curQuery) >= 4:
                self.longSessions.append(session)
        return self.longSessions

    def getLongSessionsSorted(self, length):
        """
        获取query数>= length 的sessions 并按照时间从小到大排序
        :param length: session length
        :return:
        """
        for session in self.sessions:
            interactionNum = list(session.getElementsByTagName("interaction")).__len__()
            curQuery = list(session.getElementsByTagName("currentquery")).__len__()
            if (interactionNum + curQuery) >= 4:
                self.longSessions.append(session)
        if self.year == 12:
            for i in range(self.longSessions.__len__()):
                for j in range(i + 1, self.longSessions.__len__()):
                    k = self.longSessions[i]
                    tt = self.longSessions[i].getAttribute("starttime")[0:-7]
                    st1 = dt.datetime.strptime(tt, "%H:%M:%S").time()
                    tt = self.longSessions[j].getAttribute("starttime")[0:-7]
                    st2 = dt.datetime.strptime(tt, "%H:%M:%S").time()
                    if st1 > st2:
                        self.longSessions[i], self.longSessions[j] = self.longSessions[j], self.longSessions[i]
        elif self.year == 13:
            for i in range(self.longSessions.__len__()):
                for j in range(i + 1, self.longSessions.__len__()):
                    it1 = self.longSessions[i].getElementsByTagName("interaction")
                    st1 = float(it1[0].getAttribute("starttime"))
                    it2 = self.longSessions[j].getElementsByTagName("interaction")
                    st2 = float(it2[0].getAttribute("starttime"))
                    if st1 > st2:
                        self.longSessions[i], self.longSessions[j] = self.longSessions[j], self.longSessions[i]
        return self.longSessions

    def divideAccordingTopic(self):
        """
        将某年的sessiontrack数据按照topic划分
        :return: 字典，key是tpoic编号，value是该topic下按时间顺序排好的session列表
        """
        # 依据不同年份处理数据将每个topic中的session 按照开始时间进行排序

        sortedDict = {}
        for session in self.sessions:
            topic = session.getElementsByTagName("topic")
            if self.year == 12:
                tt = session.getAttribute("starttime")[0:-7]
                # 转化为秒数
                st = dt.datetime.strptime(tt, "%H:%M:%S").time()
            elif self.year == 13:
                st = float(session.getAttribute("starttime"))
            topicId = topic[0].getAttribute("num")
            if topicId not in sortedDict.keys():
                sortedDict[topicId] = []
            sortedDict[topicId].append((st, session))

        for k in sortedDict.keys():
            temp = list(sortedDict[k])
            for j in range(temp.__len__()):
                if j == (temp.__len__() - 1):
                    break
                curKey = temp[j][0]
                nextKey = temp[j + 1][0]
                if nextKey < curKey:
                    x = temp[j]
                    temp[j] = temp[j + 1]
                    temp[j + 1] = x
            sortedDict[k] = temp
        if self.year == 12:
            print("[2012] grouped sessions according to topics")
        elif self.year == 13:
            print("[2013] grouped sessions according to topics")
        self.topicDict = sortedDict
        return
