# Non-Relevant & Exploration
IDX_NRR = 0
# Non-Relevant & Exploitation
IDX_NRT = 1
# Relevant & Exploration
IDX_RR = 2
# Relevant & Exploitation
IDX_RT = 3

# Code of Non-Relevant Rrelevant
IDX_NON_REL=0
IDX_REL=1
# Code of Exploration Exploitation
IDX_EXPR=0
IDX_EXPL=1


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
