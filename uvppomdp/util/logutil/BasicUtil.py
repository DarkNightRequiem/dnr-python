import os
import platform
import yaml
import abc


class BasicUtil(metaclass=abc.ABCMeta):

    def __init__(self):
        # 项目根目录
        self.root = os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.realpath(__file__)
                )
            )
        )

        # 配置文件路径
        if platform.system() == "Windows":
            self.cfg = yaml.load(
                open(self.root + "\\config.yaml", "rb")
            )
        elif platform.system() == "Linux":
            self.cfg = yaml.load(
                open(self.root + "/config.yaml", "rb")
            )

    @abc.abstractmethod
    def read(self,name):
        """
        读取单个文件内的所有内容
        :param name: 文件名
        :return:
        """

    @abc.abstractmethod
    def readall(self):
        """
        读取指定文件夹下的所有文件内容,包括字文件夹下的文件
        :param dir: 文件夹路径
        :return:
        """
