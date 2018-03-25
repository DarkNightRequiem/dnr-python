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

        self.tagNameList = ['sessiontrack2012', 'sessiontrack2013',
                            'session',
                            'topic',
                            'subject',
                            'desc',
                            'narr',
                            'interaction',
                            'query',
                            'results',
                            'result',
                            'url',
                            'clueweb09id', 'clueweb12id',
                            'title',
                            'snippet'
                            'clicked',
                            'click',
                            'rank',
                            'currentquery',
                            'query']

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
                st = session.getAttribute("starttime")[0:-7]
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
                if self.year==12:
                    curKey = dt.datetime.strptime(temp[j][0], "%H:%M:%S")
                    nextKey = dt.datetime.strptime(temp[j + 1][0], "%H:%M:%S")
                elif self.year==13:
                    curKey = temp[j][0]
                    nextKey =temp[j + 1][0]
                if nextKey < curKey:
                    x = temp[j]
                    temp[j] = temp[j + 1]
                    temp[j + 1] = x
            sortedDict[k] = temp
        if self.year == 12:
            print("[2012] grouped sessions according to topics")
        elif self.year==13:
            print("[2013] grouped sessions according to topics")
        self.topicDict = sortedDict
        return
