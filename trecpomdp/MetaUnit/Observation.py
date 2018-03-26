class Observation:
    def __init__(self,rel,expo):
        # 相关性维度 Non-Relevant Relevant
        self.rel=rel
        # 探索维度 exploration exploitation
        self.expo=expo

    def getRel(self):
        return self.rel

    def getExpo(self):
        return self.expo