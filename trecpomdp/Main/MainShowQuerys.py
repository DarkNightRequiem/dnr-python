import os
from util.TrecDomParser import TrecDomParser as tdp

if __name__ == '__main__':
    # 获取搜索日志所所在的目录
    projDir = os.path.dirname(os.path.realpath(__file__))
    projDir = os.path.split(projDir)[0]
    sessionLogPath2 = os.path.join(projDir, 'sessionlog', 'sessiontrack2012.xml')
    sessionLogPath3 = os.path.join(projDir, 'sessionlog', 'sessiontrack2013.xml')

    # 预处理获取 Long Sessions
    sessionTrack12 = tdp(sessionLogPath2, 12)
    sessionTrack13 = tdp(sessionLogPath3, 13)
    longSessions12 = sessionTrack12.getLongSessionsSorted(4)
    print("Long Sessions in Track2012 Count: ", longSessions12.__len__())
    longSessions13 = sessionTrack13.getLongSessionsSorted(4)
    print("Long Sessions in Track2013 Count: ", longSessions13.__len__())
    longSessions = tdp.concatSessions(longSessions12, longSessions13)
    print("Combined Long Sessions Count: ", longSessions.__len__())

    c=0
    for session in longSessions:
        child = list(session.childNodes)
        for i in range(child.__len__()):
            if i%2 != 0:
                temp = child[i]
                c+=1
                # TODO: 输出每个查询
                print("---")

    print("qur=ery",c)