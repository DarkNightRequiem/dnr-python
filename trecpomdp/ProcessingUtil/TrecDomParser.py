from xml.dom.minidom import parse
import xml.dom.minidom as minidom
import datetime as dt


# () 元组
# [] 列表
# {} 字典
# 使用dom解析xml文件

class TrecDomParser:

    def __init__(self, path):
        # 要解析的文件路径
        self.path = path
        # 文件中的DomTree
        self.domTree = minidom.parse(path)
        # 文件中的所有的dom元素
        self.collection = self.domTree.documentElement
        # 所有的<session>
        self.sessions = self.collection.getElementsByTagName("session")

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
        :return: 二维字典,第一维key是topic编号，第二维key是starttime
        """
        sortedDict = {}
        for session in self.sessions:
            topic = session.getElementsByTagName("topic")
            st=session.getAttribute("starttime")[0:-7]
            starttime = dt.datetime.strptime(st, "%H:%M:%S")
            topicId = topic[0].getAttribute("num")
            if topicId not in sortedDict.keys():
                sortedDict[topicId] = {}
            if starttime not in sortedDict[topicId]:
                sortedDict[topicId][starttime] = session
        # TODO：对字典中的session按照starttime排序
        for i in range(sortedDict.__len__()):
            s=sortedDict[str(i+1)]
        print("grouped sessions according to topics")
        return sortedDict
