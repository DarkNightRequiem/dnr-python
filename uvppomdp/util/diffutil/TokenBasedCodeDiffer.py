# --------------------------------------------
# @File     : TokenBasedCodeDiffer.py
# @Time     : 2018/6/13 15:36
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : 
# --------------------------------------------
from util.BasicUtil import BasicUtil
from util.antlr4.recognizers.CSharpLexer import CSharpLexer


class TokenBasedCodeDiffer(BasicUtil):
    def __init__(self):
        super().__init__()

        # 比较结果输出目录
        self.output_path=self.cfg.get("compile.log").get("diff.dir")["token"]

    def diff_identifier_tokens(self,from_tokens:[CSharpLexer.IDENTIFIER],to_tokens:[CSharpLexer.IDENTIFIER]):
        """

        :param from_tokens:
        :param to_tokens:
        :return:
        """
        # 去重复

        # 或许可以采用Tanimoto集合相似度进行计算
        pass



tbcode_differ=TokenBasedCodeDiffer()