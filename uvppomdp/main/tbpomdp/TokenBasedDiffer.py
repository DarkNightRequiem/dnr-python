# --------------------------------------------
# @File     : TokenBasedDiffer.py
# @Time     : 2018/6/13 16:17
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : 
# --------------------------------------------
import os
import time
import json
from util.logreader.CompileLogReader import cmpl_reader
from util.ColorfulLogger import logger
from util.antlr4.recognizers.CSharpLexer import CSharpLexer


class TokenBasedDiffer:
    def __init__(self):
        # 学生学号表
        self.stuid_list = []

        # 计数器
        self.count = 0


if __name__ == '__main__':
    tbdiffer = TokenBasedDiffer()
