# --------------------------------------------
# @File     : TokenBasedPreprocessor.py
# @Time     : 2018/6/15 21:12
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : TokenBasedPreprocessor
# --------------------------------------------
import os
import time
import json

from util.ColorfulLogger import logger
from util.ConfigReader import config_reader
from util.antlr4.recognizers.CSharpLexer import CSharpLexer
from util.logreader.CompileLogReader import cmpl_reader


class TokenBasedPreprocessor:
    def __init__(self, uploads_dir="",output_dir=""):
        # 原始编译日志存放目录
        self.uploads_dir = uploads_dir

        # 预处理结果输出目录
        self.output_dir=output_dir

        # 学生学号表
        self.stuid_list = []

        # 计数器
        self.count = 0

    def pre_process(self):
        if not os.path.exists(self.uploads_dir):
            logger.error(message="No available uploads directory found")
            exit(0)

        file_names = os.listdir(self.uploads_dir)
        for filename in file_names:
            # 对应学号和时间信息
            stuid, date, timestamp = self.get_info(filename)
            # 一名学生的一个压缩文件
            streams = cmpl_reader.read_as_zipfilestreams(self.uploads_dir+"/"+filename)
            if streams is None: continue

            all_code_tokens = []
            for stream in streams:
                # 分词
                lexer = CSharpLexer(stream)
                tokens = lexer.getAllTokens()
                code_tokens = self.get_code_tokens(tokens, lexer)
                all_code_tokens.append(code_tokens)

            # 抽取出所有的IDENTIFIER类型的token
            identifiers_tokens_text = self.get_identifiers_tokens_text(all_code_tokens)
            if identifiers_tokens_text is None: continue

            if stuid not in self.stuid_list:
                self.stuid_list.append(stuid)

            identifier_based_contents = {
                "sequenceId": self.count,
                "stuid": stuid,
                "timestamp": timestamp,
                "tokens": identifiers_tokens_text
            }

            # 写入结果
            self.write_as_json(identifier_based_contents, filename.replace(".zip", "") + ".json")
            self.count = self.count + 1

    def get_info(self,filename):
        """
        解析文件名所含有的信息
        """
        # 获取学号和日期字符串
        stuid, suffix = filename.split('-', 1)

        # 解析日期信息
        date = time.strptime(suffix.replace(".zip", ""), "%Y-%m-%d-%H-%M-%S")
        timestamp = time.mktime(date)

        return stuid, date, timestamp

    def get_code_tokens(self, tokens:list,lexer:CSharpLexer):
        code_tokens = []
        index = 0
        while index < tokens.__len__():
            token = tokens[index]
            if token.channel != lexer.HIDDEN and token.type != CSharpLexer.DIRECTIVE_NEW_LINE:
                # 当前token是代码类型
                code_tokens.append(token)

            index = index + 1

        return code_tokens

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

    def write_as_json(self,json_recognizable,filename):
        """
         写入json文件
        """
        json_content = json.dumps(json_recognizable, indent=4)
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)
        with open(
                os.path.join(
                    self.output_dir, filename
                ),
                "w",
                encoding="utf-8"
        ) as file:
            file.write(json_content)
        file.close()


if __name__ == '__main__':
    # 获取配置
    uploads_dir = config_reader.compile_logs_uploads_dir
    output_dir = config_reader.tb_tokenbasedpreprocessor_output_dir

    # 进行预处理
    preprocessor=TokenBasedPreprocessor(uploads_dir,output_dir)
    preprocessor.pre_process()
