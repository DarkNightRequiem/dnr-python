from xml.dom.minidom import parse
import xml.dom.minidom as minidom
import datetime as dt


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
    def concatSessions(s1=list, s2=list):
        """
        连接两个sessions
        :return: 连接后的sessions
        """
        s1.extend(s2)
        return s1

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
