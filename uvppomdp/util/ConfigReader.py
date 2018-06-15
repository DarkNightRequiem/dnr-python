# --------------------------------------------
# @File     : ConfigReader.py
# @Time     : 2018/6/6 21:14
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : 此文件用于读取config.yaml中的配置
# --------------------------------------------
import os
import platform
import yaml
import abc


class ConfigReader:

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

        # 所有的编译日志（zip）的存放目录
        self.uploads_dir=self.cfg.get("compile.log")["dir"]



config_reader=ConfigReader()

