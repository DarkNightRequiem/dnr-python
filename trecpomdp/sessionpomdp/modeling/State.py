# Non-Relevant & Exploration
IDX_S_NRR = 0
# Non-Relevant & Exploitation
IDX_S_NRT = 1
# Relevant & Exploration
IDX_S_RR = 2
# Relevant & Exploitation
IDX_S_RT = 3


class State:
    def __init__(self,rlv,expl):
        # 相关性维度 Relevant: True Non-Relevant: False
        self.rlv=rlv
        # 探索维度 Exploration: True Exploitation: False
        self.expl=expl

    def setRlv(self,rlv):
        self.rlv=rlv

    def setExpl(self,expl):
        self.expl=expl
