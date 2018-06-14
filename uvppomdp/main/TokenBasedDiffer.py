# --------------------------------------------
# @File     : TokenBasedDiffer.py
# @Time     : 2018/6/13 16:17
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : 
# --------------------------------------------
import os
import time
import json

from antlr4.ListTokenSource import ListTokenSource

from util.antlr4.recognizers.CSharpParser import CSharpParser
from util.diffutil.TokenBasedCodeDiffer import TokenBasedCodeDiffer
from util.logreader.CompileLogReader import cmpl_reader
from util.ColorfulLogger import logger
from util.antlr4.recognizers.CSharpLexer import CSharpLexer, CommonTokenStream


class TokenBasedDiffer(TokenBasedCodeDiffer):
    def __init__(self):
        TokenBasedCodeDiffer.__init__(self)
        # 学生学号表
        self.stuid_list = []

        # 计数器
        self.count = 0

    def pre_process(self,output=True):
        # 编译日志存放目录
        uploads_dir = cmpl_reader.dir

        if not os.path.exists(uploads_dir):
            logger.error(message="No available uploads directory found")
            exit(0)

        file_names = cmpl_reader.files_names
        for filename in file_names:
            # 对应学号和时间信息
            stuid, date, timestamp = self.get_info(filename)
            # 一名学生的一个压缩文件
            streams = cmpl_reader.read_as_zipfilestreams(filename)
            if streams is None: continue

            all_code_tokens=[]
            for stream in streams:
                # 分词
                lexer = CSharpLexer(stream)
                tokens = lexer.getAllTokens()
                code_tokens = self.get_code_tokens(tokens)
                all_code_tokens.append(code_tokens)

            # 抽取出所有的IDENTIFIER类型的token
            identifiers_tokens_text = self.get_identifiers_tokens_text(all_code_tokens)
            if identifiers_tokens_text is None: continue

            if stuid not in self.stuid_list:
                self.stuid_list.append(stuid)

            identifier_based_contents={
                    "sequenceId": self.count,
                    "stuid": stuid,
                    "timestamp": timestamp,
                    "tokens": identifiers_tokens_text
                }

            # 写入结果
            if output:
                self.write_as_json(identifier_based_contents,filename.replace(".zip","")+".json")
            self.count = self.count + 1

    def write_as_json(self,json_recognizable,filename):
        """
         写入json文件
        """
        json_content = json.dumps(json_recognizable, indent=4)
        if not os.path.exists(tbdiffer.output_path):
            os.mkdir(tbdiffer.output_path)
        with open(
                os.path.join(
                    tbdiffer.output_path, filename
                ),
                "w",
                encoding="utf-8"
        ) as file:
            file.write(json_content)
        file.close()

    def get_code_tokens(self, tokens):
        index = 0
        code_tokens = []

        while index < tokens.__len__():
            token = tokens[index]
            if token.channel != CSharpLexer.HIDDEN and token.type != CSharpLexer.DIRECTIVE_NEW_LINE:
                # 当前token是代码类型
                code_tokens.append(token)
            index = index + 1

        return code_tokens

    def diff_all(self):
        # TODO: 实现
        pass

    def get_identifiers_tokens_text(self, tokens: []):
        identifiers_tokens_text = []
        for sublist in tokens:
            for token in sublist:
                if (token.type == CSharpLexer.IDENTIFIER) and \
                        (token.text not in identifiers_tokens_text) and\
                        (token.text not in ["i","j","k","e","d","x"]):
                    identifiers_tokens_text.append(token.text)

        return identifiers_tokens_text \
            if identifiers_tokens_text.__len__() > 0 \
            else None

    def get_info(self, filename):
        """
        解析文件名所含有的信息
        """
        # 获取学号和日期字符串
        stuid, suffix = filename.split('-', 1)

        # 解析日期信息
        date = time.strptime(suffix.replace(".zip", ""), "%Y-%m-%d-%H-%M-%S")
        timestamp = time.mktime(date)

        return stuid, date, timestamp


if __name__ == '__main__':
    tbdiffer = TokenBasedDiffer()

    # 预处理
    tbdiffer.pre_process()

    print("OK")
