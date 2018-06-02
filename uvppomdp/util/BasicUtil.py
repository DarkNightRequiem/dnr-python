import os
import platform
import yaml
import abc


class BasicUtil():

    def __init__(self):
        # 项目根目录
        self.root = os.path.dirname(
                os.path.dirname(
                    os.path.realpath(__file__)
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

