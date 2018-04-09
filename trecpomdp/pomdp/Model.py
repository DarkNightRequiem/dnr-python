import abc
import random
import pprint
from datashape import with_metaclass

pp = pprint.PrettyPrinter().pprint


class Model(with_metaclass(abc.ABCMeta, object)):
    def __init__(self, argDict):
        for k in dict(argDict).keys():
            setattr(self, k, argDict[k])
        pp(argDict)

    "================= Abstract ================="
    @abc.abstractmethod
    def getActions(self):
        """
        Get all kinds of actions (discrete)
        :return:
        """

    # @abc.abstractmethod
    # def resetForSimulation(self):
    #     """
    #     Reset Model before each simulation
    #     :return:
    #     """
    #
    # @abc.abstractmethod
    # def resetForEpoch(self):
    #     """
    #     Define What to do for resetting Model before each epoch
    #     :return:
    #     """
    #
    # @abc.abstractmethod
    # def update(self,sim_data):
    #     """
    #     Update the state of the Model with sim_data
    #     :param sim_data:
    #     :return:
    #     """
    #
    # @abc.abstractmethod
    # def generateStep(self,state,action):
    #     """
    #     Generate a full step result
    #     :param state:
    #     :param action:
    #     :return:
    #     """