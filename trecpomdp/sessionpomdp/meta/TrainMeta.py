from sessionpomdp.meta.Element import Element


class TrainMata(Element):
    def __init__(self, id, state, action, observation, clickPreCount, preSat, preNsat, preClickTrueRelevant, preClickTrueNonRel):
        # 单个训练元的id: year-sessionID-topicID
        self.id = id

        # 类型为modeling.Action包含add delete keep
        self.action = action

        # 类型为modeling.Sate 包含两个维度
        self.state = state

        # 类型为modeling.Observation
        self.observation = observation

        # t-1 时刻的总点击数量
        self.clickCount = clickPreCount

        # 上一个interaction (t-1时刻的）SAT数量
        self.preSat = preSat

        # t-1 时刻的非SAT点击数量
        self.preNsat = preNsat

        # t-1 有SAT点击并且这些SAT点击确实relevant的个数
        self.preClickTrueRelevant=preClickTrueRelevant

        # t-1 只有非SAT点击并且这些非SAT点击确实不相关
        self.preClickTrueNonRelevant=preClickTrueNonRel

    def printContent(self):
        pass
