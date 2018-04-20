from sessionpomdp.meta.Element import Element


class TrainMata(Element):
    def __init__(self,id,state,action,observation):
        # 单个训练元的id: year-sessionID-topicID
        self.id=id
        # 类型为modeling.Action包含add delete keep
        self.action=action
        # 类型为modeling.Sate 包含两个维度
        self.state=state
        # 类型为modeling.Observation
        self.observation=observation

    def printContent(self):
        pass