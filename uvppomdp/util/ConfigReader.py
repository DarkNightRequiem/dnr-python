# --------------------------------------------
# @File     : ConfigReader.py
# @Time     : 2018/6/6 21:14
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : config.yaml配置文件读取器
# --------------------------------------------
import os
import platform
import yaml


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

        # 原始数据的相关配置
        self.compile_logs_uploads_dir = self.cfg["raw"]["compilelogs.uploads.dir"]
        self.search_logs_dir = self.cfg["raw"]["searchlogs.dir"]
        self.uwp_api_path = self.cfg["raw"]["uwp.api.path"]

        # 基于简单比较的POMDP的相关配置
        self.nb_naivediffer_output_dir = self.cfg["nbpomdp"]["naivediffer.output.dir"]

        # 基于Method的POMDP的相关配置
        self.mb_methodbaseddiffer_output_dir = self.cfg["mbpomdp"]["methodbaseddiffer.output.dir"]

        # 基于Token的POMDP的相关配置
        self.tb_mpquerystats_output_path=self.cfg["tbpomdp"]["statistics"]["mediaplayerquerystats.output.path"]
        self.tb_tokenbasedpreprocessor_output_dir = self.cfg["tbpomdp"]["tokenbasedpreprocessor.output.dir"]
        self.tb_tokenbasedfilter_ouput_dir = self.cfg["tbpomdp"]["tokenbasedfilter.output.dir"]
        self.tb_tokenbasedmerger_output_dir = self.cfg["tbpomdp"]["tokenbasedmerger.output.dir"]
        self.tb_tokenbaseddiffer_output_dir = self.cfg["tbpomdp"]["tokenbaseddiffer.output.dir"]
        self.tb_mediaplayer_extractor_output_dir = self.cfg["tbpomdp"]["extractor.mediaplayer.output.dir"]
        self.tb_mediaplayer_zipextractor__output_dir=self.cfg["tbpomdp"]["extractor.zip.mediaplayer.output.dir"]
        self.tb_logshrinker_output_dir=self.cfg["tbpomdp"]["logshrinker.output.dir"]
        self.tb_searchsessionextractor_output_dir=self.cfg["tbpomdp"]["searchsessionextractor.output.dir"]
        self.tb_requestactivemerger_output_dir=self.cfg["tbpomdp"]["requestactivemerger.output.dir"]


config_reader = ConfigReader()
