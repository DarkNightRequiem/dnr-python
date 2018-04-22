class UserAction:
    """
    User Domain-Level Actions
    """
    ADD_TERMS = 4
    REMOVE_TERMS = 5
    KEEP_TERMS = 6
    """
    User Communications-Level Actions
    """
    CLICKED_DOCUMENTS = 7


class EngineAction:
    """
    Engine Domain-Level Actions
    """
    INCREASE_WEIGHT = 8
    DECREASE_WEIGHT = 9
    KEEP_WEIGHT = 10

    """
    Engine Communications-Level Actions 
    """
    RETURNED_DOCUMENT = 11


class Action:
    def __init__(self, aList, rList, kList):
        # Add
        self.aList = aList
        # Remove
        self.rList = rList
        # Keep
        self.kList = kList
        # 各种动作是否存在的标志 False为不存在
        self.af=self.rf=self.kf=False
        if aList.__len__()>0:
            self.af=True
        if rList.__len__()>0:
            self.rf=True
        if kList.__len__()>0:
            self.kf=True
