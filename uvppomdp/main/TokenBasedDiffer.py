# --------------------------------------------
# @File     : TokenBasedDiffer.py
# @Time     : 2018/6/13 16:17
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : 
# --------------------------------------------
import os
import time
import json
from util.antlr4.recognizers.CSharpPreprocessorParser import CSharpPreprocessorParser
from util.diffutil.TokenBasedCodeDiffer import TokenBasedCodeDiffer
from util.logreader.CompileLogReader import cmpl_reader
from util.ColorfulLogger import logger
from util.antlr4.recognizers.CSharpLexer import CSharpLexer


class TokenBasedDiffer(TokenBasedCodeDiffer):
    def __init__(self):
        TokenBasedCodeDiffer.__init__(self)
        # 学生学号表
        self.stuid_list = []

        # 基于identifier token的所有文件内容
        self.identifier_based_contents = []

        self.count = 0

    def pre_process(self):
        # 编译日志存放目录
        uploads_dir = cmpl_reader.dir

        if not os.path.exists(uploads_dir):
            logger.error(message="No available uploads directory found")
            exit(0)

        # 获取所有学生的所有上传文件目录列表
        file_names = cmpl_reader.files_names

        for filename in file_names:
            # 一名学生的一个压缩文件
            streams = cmpl_reader.read_as_zipfilestreams(filename)
            if streams is None:
                return

            # 对应学号和时间信息
            stuid, date, timestamp = self.get_info(filename)

            identifiers_tokens = None
            for stream in streams:
                # 分词
                lexer = CSharpLexer(stream)
                tokens = lexer.getAllTokens()
                code_tokens = self.get_code_tokens(tokens)

                # 抽取出所有的IDENTIFIER类型的token
                identifiers_tokens = self.get_identifiers_tokens(code_tokens)

            if identifiers_tokens is None:
                continue

            if stuid not in self.stuid_list:
                self.stuid_list.append(stuid)

            self.identifier_based_contents.append(
                {
                    "stuid": stuid,
                    "date": date,
                    "timestamp": timestamp,
                    "tokens": identifiers_tokens
                }
            )
            print(filename)
            self.count = self.count + 1

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

    def get_identifiers_tokens(self, tokens: []):
        identifiers_tokens = []

        for token in tokens:
            if (token.type == CSharpLexer.IDENTIFIER) and \
                    (token not in identifiers_tokens):
                identifiers_tokens.append(token.text)

        return identifiers_tokens \
            if identifiers_tokens.__len__() > 0 \
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
    #tbdiffer.pre_process()

    # 写入json文件
    #json_content = json.dumps(tbdiffer.identifier_based_contents, indent=4)
    if not os.path.exists(tbdiffer.output_path):
        os.mkdir(tbdiffer.output_path)
    with open(
        os.path.join(
            tbdiffer.output_path, "identifier_based_contents.json"
        ),
        "w",
        encoding="utf-8"
    ) as file:
        file.write("dd")
    file.close()

    print("OK")
