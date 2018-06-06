import os
from util.ColorfulLogger import logger
from util.BasicUtil import BasicUtil


class MethodBasedCodeDiffer(BasicUtil):
    def __init__(self):
        BasicUtil.__init__(self)

        # 简单对比结果的存放目录
        self.naive_dir=self.cfg.get("compile.log").get("diff.dir")["naive"]

        # 对比结果输出目录
        self.output_path=self.cfg.get("compile.log")["diff.dir"]["method"]

    def method_based_diff(self):
        """
        基于方法对简单比较结果进行进一步的加工
        """
        # TODO: 实现

        pass


method_based_differ=MethodBasedCodeDiffer()