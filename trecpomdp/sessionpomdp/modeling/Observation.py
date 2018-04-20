class Observation:
    def __init__(self,rlv,expl):
        # 相关性维度 Relevant: True Non-Relevant: False
        self.rlv=rlv
        # 探索维度 Exploration: True Exploitation: False
        self.expl=expl

    def setRlv(self,rlv):
        self.rlv=rlv

    def setExpl(self,expl):
        self.expl=expl
