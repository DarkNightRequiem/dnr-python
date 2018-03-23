from xml.dom.minidom import parse
import xml.dom.minidom as minidom


# 使用dom解析xml文件

class TrecDomParser:

    def __init__(self, path):
        # 要解析的文件路径
        self.path = path
        self.domTree = minidom.parse(path)
        self.collection = self.domTree.documentElement
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
                                        'clueweb09id','clueweb12id',
                                        'title',
                                        'snippet'
                                'clicked',
                                    'click',
                                        'rank',
                            'currentquery',
                                'query']

    def getElementByTagName(self, tagName):
        """
        根据tagName获取元素
        """
        if tagName in self.tagNameList:
            elements = self.collection.getElementsByTagName(tagName)
            return elements
        else:
            return None
