# Non-Relevant & Exploration
COD_S_NRR = 0
# Non-Relevant & Exploitation
COD_S_NRT = 1
# Relevant & Exploration
COD_S_RR = 2
# Relevant & Exploitation
COD_S_RT = 3

# # Code of Non-Relevant Rrelevant
# IDX_NON_REL = 0
# IDX_REL = 1
# # Code of Exploration Exploitation
# IDX_EXPR = 0
# IDX_EXPL = 1


class State:
    def __init__(self, rlv, expl):
        # 相关性维度 Relevant: True Non-Relevant: False
        self.rlv = rlv
        # 探索维度 Exploration: True Exploitation: False
        self.expl = expl
        # 维度联合代号
        self.updateCOD()

    def setRlv(self, rlv):
        self.rlv = rlv
        self.updateCOD()

    def setExpl(self, expl):
        self.expl = expl
        self.updateCOD()

    def updateCOD(self):
        if (not self.rlv) and self.expl:
            self.COD = COD_S_NRR
        elif (not self.rlv) and (not self.expl):
            self.COD = COD_S_NRT
        elif self.rlv and self.expl:
            self.COD = COD_S_RR
        elif self.rlv and (not self.expl):
            self.COD = COD_S_RT

    def printState(self):
        if self.COD==COD_S_NRR:
            print("State: NRR",end=" ")
        elif self.COD==COD_S_NRT:
            print("State: NRT",end=" ")
        elif self.COD==COD_S_RR:
            print("State: RR",end=" ")
        elif self.COD==COD_S_RT:
            print("State: RT",end=" ")
