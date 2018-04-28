import os
from sessionpomdp.util.TrecDomParser import TrecDomParser as tdp
from sessionpomdp.util.TrainingSampleExtractor import Extractor as extc

if __name__ == '__main__':
    # 在session track2012中有一个subject是"merck & co"在6140行左右，&是特殊字符解析或报错，我先简单替换成空格，分析无影响
    # 分词工具 nltk spacy jieba lxml

    # 获取搜索日志所所在的目录
    longSessionLength = 5
    projDir = os.path.dirname(os.path.realpath(__file__))
    projDir = os.path.split(projDir)[0]
    sessionLogPath2 = os.path.join(projDir, 'sessionpomdp','sessionlog', 'sessiontrack2012.xml')
    sessionLogPath3 = os.path.join(projDir, 'sessionpomdp','sessionlog', 'sessiontrack2013.xml')

    # 预处理获取 Long Sessions
    sessionTrack12 = tdp(sessionLogPath2, 12)
    longSessions12 = sessionTrack12.getLongSessionsSorted(longSessionLength,False)
    print("Long Sessions in Track2012 Count: ", longSessions12.__len__())
    inter12=tdp.getInteractions(longSessions12, 2012)

    sessionTrack13 = tdp(sessionLogPath3, 13)
    longSessions13 = sessionTrack13.getLongSessionsSorted(longSessionLength,False)
    print("Long Sessions in Track2013 Count: ", longSessions13.__len__())
    inter13=tdp.getInteractions(longSessions13, 2013)

    print("Combined Long Sessions Count: ", longSessions12.__len__()+longSessions13.__len__())

    # 生成interaction列表
    interList=tdp.concat(inter12, inter13)
    # 生成训练样本
    sample=extc.getTrainingSample(interList)

    print("--End--")
