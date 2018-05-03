# Non-Relevant & Exploration
COD_O_NRR = 0
# Non-Relevant & Exploitation
COD_O_NRT = 1
# Relevant & Exploration
COD_O_RR = 2
# Relevant & Exploitation
COD_O_RT = 3


class Observation:
    def __init__(self,rlv,expl):
        # 相关性维度 Relevant: True    Non-Relevant: False
        self.rlv=rlv
        # 探索维度 Exploration: True   Exploitation: False
        self.expl=expl
        self.updateCOD()

    def setRlv(self,rlv):
        self.rlv=rlv
        self.updateCOD()

    def setExpl(self,expl):
        self.expl=expl
        self.updateCOD()

    def updateCOD(self):
        if (not self.rlv) and self.expl:
            self.COD = COD_O_NRR
        elif (not self.rlv) and (not self.expl):
            self.COD = COD_O_NRT
        elif self.rlv and self.expl:
            self.COD = COD_O_RR
        elif self.rlv and (not self.expl):
            self.COD = COD_O_RT

    def printObsrv(self):
        if not self.rlv and self.expl:
            print("Observ: NRR",end=" ")
        elif not self.rlv and not self.expl:
            print("Observ: NRT",end=" ")
        elif self.rlv and self.expl:
            print("Observ: RR",end=" ")
        elif self.rlv and not self.expl:
            print("Observ: RT",end=" ")