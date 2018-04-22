import os

from sessionpomdp.util.TrecDomParser import TrecDomParser as tdp

if __name__ == '__main__':
    # 获取搜索日志所所在的目录
    projDir = os.path.dirname(os.path.realpath(__file__))
    projDir = os.path.split(projDir)[0]
    sessionLogPath2 = os.path.join(projDir,'sessionpomdp', 'sessionlog', 'sessiontrack2012.xml')
    sessionLogPath3 = os.path.join(projDir,'sessionpomdp','sessionlog', 'sessiontrack2013.xml')

    # 预处理获取 Long Sessions
    longSessionLength = 4
    sessionTrack12 = tdp(sessionLogPath2, 12)
    sessionTrack13 = tdp(sessionLogPath3, 13)
    longSessions12 = sessionTrack12.getLongSessionsSorted(longSessionLength,False)
    print("Long Sessions in Track2012 Count: ", longSessions12.__len__())
    longSessions13 = sessionTrack13.getLongSessionsSorted(longSessionLength,False)
    print("Long Sessions in Track2013 Count: ", longSessions13.__len__())
    longSessions = tdp.concat(longSessions12, longSessions13)
    print("Combined Long Sessions Count: ", longSessions.__len__())

    print("\n==================All Query in 2012&2013 Long Sessions=======================\n")
    c = 0
    for session in longSessions:
        child = list(session.childNodes)
        for i in range(child.__len__()):
            if (i % 2 != 0) and (i>=3):
                temp = child[i]
                q = temp.getElementsByTagName("query")[0]
                tx = q.childNodes[0].data
                c += 1
                print(tx)

    print("\n=========================================\n","Total: ", c)
