from pomdp.Actions import DiscreteAction


class UserAction:
    """
    User Domain-Level Actions
    """
    ADD_TERMS = 0
    REMOVE_TERMS = 1
    KEEP_TERMS = 2
    """
    User Communications-Level Actions
    """
    CLICKED_DOCUMENTS = 3


class EngineAction:
    """
    Engine Domain-Level Actions
    """
    INCREASE_WEIGHT = 4
    DECREASE_WEIGHT = 5
    KEEP_WEIGHT = 6

    """
    Engine Communications-Level Actions 
    """
    RETURNED_DOCUMENT = 7


class AgentAction(DiscreteAction):
    def printAction(self):
        if self.binCode is UserAction.ADD_TERMS:
            action = "User add terms"
        elif self.binCode is UserAction.REMOVE_TERMS:
            action = "User remove terms"
        elif self.binCode is UserAction.KEEP_TERMS:
            action = "User keep terms"
        elif self.binCode is UserAction.CLICKED_DOCUMENTS:
            action = "User click a document"
        elif self.binCode is EngineAction.INCREASE_WEIGHT:
            action = "Engine increase weight"
        elif self.binCode is EngineAction.DECREASE_WEIGHT:
            action = "Engine decrease weight"
        elif self.binCode is EngineAction.KEEP_WEIGHT:
            action = "Engine keep weight"
        elif self.binCode is EngineAction.RETURNED_DOCUMENT:
            action = "Engine return ranked documents"
        else:
            action = "User unknown action"
        print(action)

    def toString(self):
        if self.binCode is UserAction.ADD_TERMS:
            action = "User add terms"
        elif self.binCode is UserAction.REMOVE_TERMS:
            action = "User remove terms"
        elif self.binCode is UserAction.KEEP_TERMS:
            action = "User keep terms"
        elif self.binCode is UserAction.CLICKED_DOCUMENTS:
            action = "User click a document"
        elif self.binCode is EngineAction.INCREASE_WEIGHT:
            action = "Engine increase weight"
        elif self.binCode is EngineAction.DECREASE_WEIGHT:
            action = "Engine decrease weight"
        elif self.binCode is EngineAction.KEEP_WEIGHT:
            action = "Engine keep weight"
        elif self.binCode is EngineAction.RETURNED_DOCUMENT:
            action = "Engine return ranked documents"
        else:
            action = "User unknown action"
        return action
