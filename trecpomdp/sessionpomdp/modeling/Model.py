from __future__ import division
import pprint as pp
import numpy as np
from sessionpomdp.modeling.State import IDX_NRR,IDX_NRT,IDX_RR,IDX_RT,IDX_EXPR,IDX_EXPL,IDX_NON_REL,IDX_REL

"""
iteration： 数据进行一次前向-后向的训练（也就是更新一次参数）
batchsize：每次迭代（iteration）训练图片的数量
epoch：1个epoch就是将所有的训练图像全部通过网络训练一次
例如：假如有1280000张图片，batchsize=256，则1个epoch需要1280000/256=5000次iteration
假如它的max-iteration=450000，则共有450000/5000=90个epoch
"""


class SessionSearchModel:
    def __init__(self,argDict):
        # state number, in this case,4
        self.stateNum=argDict["stateNum"]
        # action的种数
        self.actionNum=argDict["actionNum"]
        # discount factor
        self.discount=argDict["discount"]
        # 训练数据
        self.trainMetaList= argDict['trainMetaList']
        # 计算 相关性维度 观测函数
        self.O_Rel = self.getObservationFunction_REL()
        # TODO: 计算探索性维度 观测函数
        # TODO: 计算状态转移函数
        # TODO: 计算初始的belief state
        # 初始化belief space
        self.space=self.getInitBeliefSpace()


    def getInitBeliefSpace(self):
        bp=np.zeros(self.stateNum,dtype=np.float)
        # TODO: 根据论文修改
        bp[IDX_NRR]=1
        bp[IDX_NRT]=0
        bp[IDX_RR]=0
        bp[IDX_RT]=0
        print("Initial Belief Space:",bp)
        return bp

    def getObservationFunction_REL(self):

        # p_r_r p_n_r  p_sat  p_nsat
        p_r_r=0.0
        p_n_r=0.0
        p_r_n=0.0
        p_n_n=0.0
        p_sat=0.0
        p_nsat=0.0

        # t-1时刻存在SAT点击的Interation的个数
        totalPreSat_Inter=0
        # t-1时刻不存在SAT点击的Intaraction的个数
        totalPreNsat_Inter=0

        # t-1的结果中至少有SAT点击并且这些点击确实relevant的Interaction的个数
        trueRelevant=0

        id=self.trainMetaList[0].id

        for i in range(self.trainMetaList.__len__()):
            meta=self.trainMetaList[i]
            if meta.preSat>0:
                totalPreSat_Inter+=1
            else:
                totalPreNsat_Inter+=1

            trueRelevant+=meta.preClickTrueRelevant

        p_sat=totalPreSat_Inter/self.trainMetaList.__len__()
        p_nsat=totalPreNsat_Inter/self.trainMetaList.__len__()
        p_r_r=trueRelevant/totalPreSat_Inter
        p_n_r=1-p_r_r
        p_r_n=trueRelevant/totalPreNsat_Inter
        p_n_n=1-p_r_n

        # s=Rel w=Rel  => p_r_r * p_sat
        O_r_r=p_r_r*p_sat
        # s=N-Rel w=Rel => p_n_r * p_sat
        O_n_r=p_n_r*p_sat
        # s=Rel w=N-Rel => p_r_n * p_nsat
        O_r_n=p_r_n*p_nsat
        # s=N-Rel w=N-Rel => p_n_n * p_nsat
        O_n_n=p_n_n*p_nsat
        print("Calculate Relevance Observation Function")

        return np.array([[O_n_n,O_n_r],
                         [O_r_n,O_r_r]])

    def getObservationFunction_EXPL(self):
        # TODO:实现
        pass

"""
    argDict = dict()
    argDict['stateNum'] = 4
    argDict['actionNum'] = 3  # TODO: 通过数据预处理获得user agent的数量
    argDict['discount'] = 0.95
    argDict['trainMetaList']=trainMetaList
"""