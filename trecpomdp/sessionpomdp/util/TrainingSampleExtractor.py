import datetime as dt
from sessionpomdp.meta.Click import Click
from sessionpomdp.meta.Interaction import Interaction
from sessionpomdp.meta.Result import Result
from sessionpomdp.meta.TrainMeta import TrainMata
from sessionpomdp.modeling.State import State
from sessionpomdp.modeling.Observation import Observation


class Extractor:
    @staticmethod
    def getTrainingSample(interactions):
        trainingDict={}
        for interaction in interactions:
            if type(interaction)!=Interaction:
                continue
            ky=str(interaction.year)+"-"+str(interaction.sessionID)+"-"+str(interaction.topicID)
            if ky in trainingDict.keys():
                trainingDict[ky].append(interaction)
            else:
                trainingDict[ky]=[]
                trainingDict[ky].append(interaction)

        # TODO: 计算 Action和真实state和observation
        for ky in trainingDict.keys():
            itList=trainingDict[ky]
            for i in range(itList.__len__()):
                #inter=itList[i]
                if type(itList[i])!=Interaction:
                    continue

                '------做观测------'
                s = Observation(False, True)

                # 做相关性维度的观测
                if i==0:
                    # 一个session的第一个interaction
                    print("s")
                elif itList[i].isSessionEnd:
                    # 一个session的最后一个interaction making worthless
                    continue
                else:
                    if itList[i-1].clickedSAT>0:
                        # t-1时刻有SAT点击,t时刻观测为Relevant
                        s.setRlv(True)
                    else:
                        # 否则观测为Non-Relevant
                        s.setRlv(False)

                # 做探索维度的观测
                # TODO: 扒网页啊

        return None


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