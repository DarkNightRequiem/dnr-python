from pomdp.Actions import DiscreteAction


class UserAction:
    """
    User agent Domain-Level Actions
    """
    ADD_TERMS = 0
    REMOVE_TERMS = 1
    KEEP_TERMS = 2
    """
    User agent Communications-Level Actions
    """
    CLICKED_DOCUMENTS = 3


class EngineAction:
    """
    Search Engine Domain-Level Actions
    """
    INCREASE_WEIGHT = 4
    DECREASE_WEIGHT = 5
    KEEP_WEIGHT = 6


class AgentAction(DiscreteAction):
    def printAction(self):
        # TODO: 实现抽象函数
        pass

    def toString(self):
        # TODO: 实现抽象函数
        pass
