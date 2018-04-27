import datetime as dt
from sessionpomdp.meta.Click import Click
from sessionpomdp.meta.Interaction import Interaction
from sessionpomdp.meta.Result import Result
from sessionpomdp.meta.TrainMeta import TrainMata
from sessionpomdp.modeling.State import State
from sessionpomdp.modeling.Observation import Observation
from sessionpomdp.modeling.Action import Action
from sessionpomdp.util.rlvMap import rlvDict
from sessionpomdp.util.explMap import explDict12, explDict13


class Extractor:
    @staticmethod
    def getTrainingSample(interactions):
        trainMetaList = []
        trainingDict = {}
        for interaction in interactions:
            if type(interaction) != Interaction:
                continue
            ky = str(interaction.year) + "-" + str(interaction.sessionID) + "-" + str(interaction.topicID)
            if ky in trainingDict.keys():
                trainingDict[ky].append(interaction)
            else:
                trainingDict[ky] = []
                trainingDict[ky].append(interaction)

        for ky in trainingDict.keys():
            itList = trainingDict[ky]
            for i in range(itList.__len__()):
                # inter=itList[i]
                if type(itList[i]) != Interaction:
                    continue
                id = str(itList[i].year) + "-" + str(itList[i].sessionID) + "-" + str(itList[i].topicID)

                # 计算 Action和真实state和observation, SAT点击的相关计数
                o = Observation(None, None)
                s = State(None, None)
                a = None

                if i == 0:
                    # 赋予初始的state,action
                    # 每个session的第一个interaction总是Non-Relevant Exploration
                    s.setRlv(False)
                    s.setExpl(True)
                    a = None
                    o = None
                    trainMetaList.append(TrainMata(id, s, a, o, 0, 0, 0, 0,0))
                    continue
                elif itList[i].isSessionEnd:
                    # 一个session的最后一个interaction 没有意义
                    continue
                else:
                    # ---计算Action (query change)
                    l = Extractor.calQueryChanges(itList[i].query, itList[i - 1].query)
                    a = Action(l[0], l[1], l[2])

                    # ---做相关性维度观测
                    if itList[i - 1].clickedSAT > 0:
                        # t-1时刻有SAT点击,t时刻观测为Relevant
                        o.setRlv(True)
                    else:
                        # 否则观测为Non-Relevant
                        o.setRlv(False)

                    # ---做探索性维度观测
                    if not (a.aList is None or itList[i - 1].results is None):
                        ef = Extractor.isInPreResults(a.aList, itList[i - 1].results)
                    if (a.af and not ef) or ((not a.af) and a.rf):
                        # add不为空并且add不在之前的result中 或 add为空且remove不为空 则为Exploration
                        o.setExpl(True)
                    elif (a.af and ef) or (not a.af and not a.rf):
                        # add不为空并且add在之前的result中 或 add为空且remove为空 则为Exploitation
                        o.setExpl(False)

                    # ---标记真实的state的relevance
                    sf = False
                    for res in itList[i].results:
                        key = itList[i].topicID + "*" + res.webID
                        if key in rlvDict.keys():
                            if rlvDict[key] >= 3:
                                sf = True
                            else:
                                sf = False
                        else:
                            sf = True
                    s.setRlv(sf)

                    # ---标记真实的state的expl
                    if itList[i].year == 2012:
                        d = explDict12
                    elif itList[i].year == 2013:
                        d = explDict13
                    k1 = str(itList[i].sessionID)
                    k2 = str(itList[i].position) + "*" + str(itList[i].query)
                    if d[k1][k2] == 'R':
                        s.setExpl(True)
                    elif d[k1][k2] == 'T':
                        s.setExpl(False)

                    # ---计算t-1时刻true relevant click
                    if Extractor.isPreTrueRelevant(itList[i-1].results,itList[i-1].clicked):
                        preTrueRel=1
                    else:
                        preTrueRel=0

                    # ---计算t-1时刻true non relevant click
                    if Extractor.isPreTrueRelevant(itList[i-1].results,itList[i-1].clicked):
                        preTrueNonRel=1
                    else:
                        preTrueNonRel=0
                    # ---生成训练元数据并加入列表
                    trainMetaList.append(TrainMata(id, s, a, o,
                                                   itList[i - 1].clickedSAT + itList[i - 1].clickedNonSAT,
                                                   itList[i - 1].clickedSAT,
                                                   itList[i - 1].clickedNonSAT,preTrueRel,preTrueNonRel))

        return trainMetaList

    @staticmethod
    def calQueryChanges(qNow, qPre):
        # 去掉首尾的空格并将一些特殊字符去掉
        q1 = qPre.strip().replace("\"", "").replace(".", "").replace(";", "").replace("&", "").replace(":", "")
        q2 = qNow.strip().replace("\"", "").replace(".", "").replace(";", "").replace("&", "").replace(":", "")

        # 进行分割
        a1 = q1.split(" ")
        a2 = q2.split(" ")

        # 记录A R K
        aList = []
        rList = []
        kList = []
        for term in a1:
            if term in q2:
                # 找 k
                kList.append(term)
                q1.replace(term, "")
                q2.replace(term, "")
            elif term not in q2:
                # 找 R
                rList.append(term)
        # 找A
        for term in a2:
            if term not in q1:
                aList.append(term)

        return aList, rList, kList

    @staticmethod
    def isInPreResults(xList, preResults):
        if preResults is None or xList is None:
            return False
        f = True
        for term in xList:
            for res in preResults:
                if res is None or res.snippet is None or term is None:
                    f = False
                elif term in res.snippet:
                    f = True
        return f

    @staticmethod
    def isPreTrueRelevant(preResults, preClick):
        if preResults is None or preClick is None:
            return 0
        f = False
        ranks = []
        for cl in preClick:
            if cl.isSAT and cl.rank not in ranks:
                ranks.append(cl.rank)

        for rank in ranks:
            for res in preResults:
                if rank == res.rank:
                    if res.relevance:
                        f = True
        return f

    @staticmethod
    def isPreTrueNonRelevant(preResults, preClick):
        if preResults is None or preClick is None:
            return True
        f = False
        ranks = []
        for cl in preClick:
            if not cl.isSAT and cl.rank not in ranks:
                ranks.append(cl.rank)

        for rank in ranks:
            for res in preResults:
                if rank == res.rank:
                    if not res.relevance:
                        f = True
        return f


"""
        self.year = it["year"]
        self.topicID = it["topicID"]
        self.topic = it["topic"]
        self.query = it["query"]
        self.results = it["results"]
        self.clicked = it["clicked"]
        self.isSessionEnd = it["isSessionEnd"]
        self.position = it["position"]
        self.sessionID = it["sessionID"]

        # 计算 exploration dimension True: exploration False: exploitation
        self.expl = self.calExplo(self.sessionID, self.position, self.year,self.query)
        # clicked 中的SAT的个数和非SAT的个数
        self.clickedSAT,self.clickedNonSAT=self.countSAT(self.clicked)
"""
