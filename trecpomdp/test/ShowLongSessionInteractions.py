import os

from sessionpomdp.util.TrecDomParser import TrecDomParser as tdp

if __name__ == '__main__':
    # 在session track2012中有一个subject是"merck & co"在6140行左右，&是特殊字符解析或报错，我先简单替换成空格，分析无影响

    # 获取搜索日志所所在的目录
    projDir = os.path.dirname(os.path.realpath(__file__))
    projDir = os.path.split(projDir)[0]
    sessionLogPath2 = os.path.join(projDir, 'sessionpomdp','sessionlog', 'sessiontrack2012.xml')
    sessionLogPath3 = os.path.join(projDir, 'sessionpomdp','sessionlog', 'sessiontrack2013.xml')

    # 预处理获取 Long Sessions
    longSessionLength = 9
    sessionTrack12 = tdp(sessionLogPath2, 12)
    longSessions12 = sessionTrack12.getLongSessionsSorted(longSessionLength,False)
    sample12=tdp.getInteractions(longSessions12, 2012)

    sessionTrack13 = tdp(sessionLogPath3, 13)
    longSessions13 = sessionTrack13.getLongSessionsSorted(longSessionLength,False)
    sample13=tdp.getInteractions(longSessions13, 2013)

    # 生成interaction列表作为训练的样本
    sampleList=tdp.concat(sample12, sample13)

    for samp in sampleList:
        samp.printContent()
