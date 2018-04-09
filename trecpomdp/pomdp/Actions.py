import abc

class DiscreteAction:
    def __init__(self, binCode):
        self.binCode = binCode

    def __hash__(self):
        return self.binCode

    def __eq__(self, other_discrete_action):
        return self.binCode == other_discrete_action.binCode

    @abc.abstractmethod
    def printAction(self):
        """
        print the aciton type
        :return:
        """

    @abc.abstractmethod
    def toString(self):
        """
        return the action type (String)
        :return:
        """