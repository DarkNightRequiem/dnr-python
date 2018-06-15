# --------------------------------------------
# @File     : TokenBasedDiffer.py
# @Time     : 2018/6/13 16:17
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : 
# --------------------------------------------
import os
import time
import json
from util.diffutil.TokenBasedCodeDiffer import TokenBasedCodeDiffer
from util.logreader.CompileLogReader import cmpl_reader
from util.ColorfulLogger import logger
from util.antlr4.recognizers.CSharpLexer import CSharpLexer


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
                code_tokens = self.get_code_tokens(tokens,lexer)
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





if __name__ == '__main__':
    tbdiffer = TokenBasedDiffer()

    # 预处理
    tbdiffer.pre_process()

    print("OK")
