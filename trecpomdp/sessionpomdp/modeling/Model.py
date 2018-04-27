from __future__ import division
import pprint as pp
import numpy as np
from sessionpomdp.modeling.State import COD_S_NRR, COD_S_NRT, COD_S_RR, COD_S_RT, IDX_EXPR, IDX_EXPL, IDX_NON_REL, \
    IDX_REL
from sessionpomdp.modeling.Action import IDX_ADD, IDX_RMV, IDX_KEP, IDX_APR,IDX_CLK

"""
iteration： 数据进行一次前向-后向的训练（也就是更新一次参数）
batchsize：每次迭代（iteration）训练图片的数量
epoch：1个epoch就是将所有的训练图像全部通过网络训练一次
例如：假如有1280000张图片，batchsize=256，则1个epoch需要1280000/256=5000次iteration
假如它的max-iteration=450000，则共有450000/5000=90个epoch
"""


class SessionSearchModel:
    def __init__(self, argDict):
        # state number, in this case,4
        self.stateNum = argDict["stateNum"]

        # action的种数
        self.actionNum = argDict["actionNum"]

        # discount factor
        self.discount = argDict["discount"]

        # 训练数据
        self.trainMetaList = argDict['trainMetaList']

        # 计算 相关性维度 观测函数
        self.O_Rel = self.getObservationFunction_REL()

        # 计算探索性维度 观测函数
        self.O_EXPL_ADD, \
        self.O_EXPL_RMV, \
        self.O_EXPL_KEP, \
        self.O_EXPL_APR = self.getObservationFunction_EXPL()

        # 计算两个维度联合的观测函数(这种矩阵暂时没用,并且只有在两个维度相互独立的情况下才存在)
        self.oADD, \
        self.oRMV, \
        self.oKEP,\
        self.oAPR= self.getJointObservationFunction()

        # 计算状态转移函数
        self.T = self.getTransitionMatirx()

        # 初始化belief space
        self.space = self.getInitBeliefSpace()

    def getInitBeliefSpace(self):
        """
        计算初始的belief space 对所有的session
        """
        bp = np.zeros(self.stateNum, dtype=np.float)
        countNR = countR = countER = countEL = 0
        for meta in self.trainMetaList:
            code = meta.state.COD
            if code == COD_S_NRR:
                countNR += 1
                countER += 1
            elif code == COD_S_NRT:
                countNR += 1
                countEL += 1
            elif code == COD_S_RR:
                countR += 1
                countER += 1
            elif code == COD_S_RT:
                countR += 1
                countEL += 1
        p_NR = countNR / self.trainMetaList.__len__()
        p_R = countR / self.trainMetaList.__len__()
        p_ER = countER / self.trainMetaList.__len__()
        p_EL = countEL / self.trainMetaList.__len__()

        bp[COD_S_NRR] = p_NR * p_ER
        bp[COD_S_NRT] = p_NR * p_EL
        bp[COD_S_RR] = p_R * p_ER
        bp[COD_S_RT] = p_R * p_EL

        print("===================================================\n"
              "Initial Belief Space:"
              "\n===================================================")
        print(bp)
        return bp

    def getObservationFunction_REL(self):
        """
        计算相关性维度的Observation Function
        """
        # t-1时刻存在SAT点击的Interation的个数
        totalPreSat_Inter = 0
        # t-1时刻不存在SAT点击的Intaraction的个数
        totalPreNsat_Inter = 0

        # t-1的结果中至少有SAT点击并且这些点击确实relevant的Interaction的个数
        trueRelevant = 0
        # t-1中只有非SAT点击并且这些非SAT点击确实不相关
        trueNonRelevant = 0

        id = self.trainMetaList[0].id

        for i in range(self.trainMetaList.__len__()):
            meta = self.trainMetaList[i]
            if meta.preSat > 0:
                totalPreSat_Inter += 1
            else:
                totalPreNsat_Inter += 1

            trueRelevant += meta.preClickTrueRelevant
            trueNonRelevant += meta.preClickTrueNonRelevant

        p_sat = totalPreSat_Inter / self.trainMetaList.__len__()
        p_nsat = totalPreNsat_Inter / self.trainMetaList.__len__()
        p_r_r = trueRelevant / totalPreSat_Inter
        p_n_n = trueNonRelevant / totalPreNsat_Inter

        # s=Rel w=Rel  => p_r_r * p_sat
        O_r_r = p_r_r * p_sat
        # s=N-Rel w=N-Rel => p_n_n * p_nsat
        O_n_n = p_n_n * p_nsat
        # s=N-Rel w=Rel => p_n_r * p_sat
        O_n_r = 1 - O_n_n
        # s=Rel w=N-Rel => p_r_n * p_nsat
        O_r_n = 1 - O_r_r

        res = np.array([[O_n_n, O_n_r],
                        [O_r_n, O_r_r]])

        print("===================================================\n"
              "Observation Function-[Relevance Dimension]:"
              "\n===================================================")
        pp.pprint(res)
        return res

    def getObservationFunction_EXPL(self):
        """
        计算探索性维度的Observation Function
        """
        trueExploitation = 0
        observedExploitation = 0
        trueExploration = 0
        observedExploration = 0
        total_add_el = true_add_el = total_add_er = true_add_er = 0
        total_rmv_el = true_rmv_el = total_rmv_er = true_rmv_er = 0
        total_kep_el = true_kep_el = total_kep_er = true_kep_er = 0
        total_apr_el = true_apr_el = total_apr_er = true_apr_er = 0

        for meta in self.trainMetaList:
            if meta.observation is None:
                continue

            if not meta.observation.expl:
                # 观测是 exploitation
                observedExploitation += 1
                if meta.action is not None:
                    if meta.action.af:
                        total_add_el += 1
                    if meta.action.rf:
                        total_rmv_el += 1
                    if meta.action.kf:
                        total_kep_el += 1
                    if meta.action.arf:
                        total_apr_el += 1

                if not meta.state.expl:
                    # 实际上也是 exploitation
                    trueExploitation += 1
                    if meta.action is not None:
                        if meta.action.af:
                            true_add_el += 1
                        if meta.action.rf:
                            true_rmv_el += 1
                        if meta.action.kf:
                            true_kep_el += 1
                        if meta.action.arf:
                            true_apr_el += 1

            else:
                # 观测是exploration
                observedExploration += 1
                if meta.action is not None:
                    if meta.action.af:
                        total_add_er += 1
                    if meta.action.rf:
                        total_rmv_er += 1
                    if meta.action.kf:
                        total_kep_er += 1
                    if meta.action.arf:
                        total_apr_er += 1

                if meta.state.expl:
                    # 实际上也是exploration
                    trueExploration += 1
                    if meta.action is not None:
                        if meta.action.af:
                            true_add_er += 1
                        if meta.action.rf:
                            true_rmv_er += 1
                        if meta.action.kf:
                            true_kep_er += 1
                        if meta.action.arf:
                            true_apr_er += 1

        p_el_el = trueExploitation / observedExploitation
        # p_er_el = 1 - p_el_el
        p_er_er = trueExploration / observedExploration
        # p_el_er = 1 - p_er_er

        p_er_add = p_er_rmv = p_er_kep = p_er_apr = 0

        if true_add_el == 0 or total_add_el == 0:
            p_el_add = 0
        else:
            p_el_add = true_add_el / total_add_el
            if total_add_er != 0:
                p_er_add = true_add_er / total_add_er

        if true_rmv_el == 0 or total_rmv_el == 0:
            p_el_rmv = 0
        else:
            p_el_rmv = true_rmv_el / total_rmv_el
            if total_rmv_er != 0:
                p_er_rmv = true_rmv_er / total_rmv_er

        if true_kep_el == 0 or total_rmv_el == 0:
            p_el_kep = 0
        else:
            p_el_kep = true_kep_el / total_kep_el
            if total_kep_er != 0:
                p_er_kep = true_kep_er / total_kep_er

        if true_apr_el == 0 or total_apr_el == 0:
            p_el_apr = 0
        else:
            p_el_apr = true_apr_el / total_apr_el
            if total_apr_er != 0:
                p_er_apr = true_apr_er / total_apr_er

        # 计算ADD观测
        O_EXPL_ADD = np.array([[p_er_er * p_er_add, 1 - p_er_er * p_er_add],
                               [1 - p_el_el * p_el_add, p_el_el * p_el_add]])
        # 计算REMOVE观测
        O_EXPL_RMV = np.array([[p_er_er * p_er_rmv, 1 - p_er_er * p_er_rmv],
                               [1 - p_el_el * p_el_rmv, p_el_el * p_el_rmv]])

        # 计算KEEP观测
        O_EXPL_KEP = np.array([[p_er_er * p_er_kep, 1 - p_er_er * p_er_kep],
                               [1 - p_el_el * p_el_kep, p_el_el * p_el_kep]])

        # 计算KEEP观测
        O_EXPL_APR = np.array([[p_er_er * p_er_apr, 1 - p_er_er * p_er_apr],
                               [1 - p_el_el * p_el_apr, p_el_el * p_el_apr]])

        print("===================================================\n"
              "Observation Function-[Explore Dimension]:"
              "\n===================================================")
        pp.pprint(O_EXPL_ADD)
        pp.pprint(O_EXPL_RMV)
        pp.pprint(O_EXPL_KEP)
        pp.pprint(O_EXPL_APR)
        return O_EXPL_ADD, O_EXPL_RMV, O_EXPL_KEP, O_EXPL_APR

    def getJointObservationFunction(self):
        O_ADD = self.O_Rel * self.O_EXPL_ADD
        O_RMV = self.O_Rel * self.O_EXPL_RMV
        O_KEP = self.O_Rel * self.O_EXPL_KEP
        O_APR=self.O_Rel* self.O_EXPL_APR
        return O_ADD, O_RMV, O_KEP,O_APR

    def getTransitionMatirx(self):
        """
        构建状态转移函数
        """
        # 初始化构建
        transition = np.zeros((self.actionNum, self.stateNum, self.stateNum))
        countTable = np.zeros((self.stateNum, self.actionNum, self.stateNum))

        # 构建 countTable
        for i in range(self.trainMetaList.__len__() - 1):
            metaNow = self.trainMetaList[i]
            metaNext = self.trainMetaList[i + 1]
            if metaNext.action is None:
                continue
            if metaNext.action.af:
                countTable[metaNow.state.COD][IDX_ADD][metaNext.state.COD] += 1
            if metaNext.action.rf:
                countTable[metaNow.state.COD][IDX_RMV][metaNext.state.COD] += 1
            if metaNext.action.kf:
                countTable[metaNow.state.COD][IDX_KEP][metaNext.state.COD] += 1
            if metaNext.action.arf:
                countTable[metaNow.state.COD][IDX_APR][metaNext.state.COD] += 1
            if metaNext.clickCount>0:
                countTable[metaNow.state.COD][IDX_CLK][metaNext.state.COD]+=1

        # pp.pprint(countTable)

        # 生成Transition
        # np.seterr(divide='ignore')
        for i in range(self.actionNum):
            for j in range(self.stateNum):
                for k in range(self.stateNum):
                    if np.sum(countTable[j][i]) == 0:
                        transition[i][j][k] = 0
                    else:
                        transition[i][j][k] = countTable[j][i][k] / np.sum(countTable[j][i])

        print("===================================================\n"
              "Model Trasition [actionNum][stateNum][stateNum]:"
              "\n===================================================")
        pp.pprint(transition)
        return transition

    def updateBeleifSpace(self, O, T):
        """
        belief update 函数
        :param O:
        :param T:
        :return:
        """
        # TODO: 实现
        pass
