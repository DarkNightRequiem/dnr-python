# --------------------------------------------
# @File     : TestAntlr.py
# @Time     :
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : Generated Before I set template
# --------------------------------------------
import sys

import chardet
from antlr4 import *
from antlr4.ListTokenSource import ListTokenSource
from util.antlr4.recognizers.CSharpLexer import CSharpLexer
from util.antlr4.recognizers.CSharpParser import CSharpParser
from util.antlr4.recognizers.CSharpParserListener import CSharpParserListener
from util.antlr4.recognizers.CSharpParserVisitor import CSharpParserVisitor
from util.antlr4.recognizers.CSharpPreprocessorParser import CSharpPreprocessorParser
from util.antlr4.csharpiutil.MbParserVistor import MbParserVistor


class MyListener(CSharpParserListener):
    def __init__(self):
        CSharpParserListener.__init__(self)

    def enterClass_body(self, ctx:CSharpParser.Class_bodyContext):
        # 进入
        text1=ctx.getText()
        decl=ctx.class_member_declarations()
        openbrace=ctx.OPEN_BRACE()
        closebrace=ctx.CLOSE_BRACE()
        altNumber=ctx.getAltNumber()
        payLoad= ctx.getPayload()
        ruleContext=ctx.getRuleContext()
        # assignment_token= ctx.getToken(CSharpLexer.ASSIGNMENT,0)
        print("entering Class_body")

    def exitClass_body(self, ctx:CSharpParser.Class_bodyContext):
        text2=ctx.getText()
        decl = ctx.class_member_declarations()
        print("exiting Class_body")

    def enterKeyword(self, ctx:CSharpParser.KeywordContext):
        print("entering Keyword")

    def exitKeyword(self, ctx:CSharpParser.KeywordContext):
        text= ctx.getText()
        print("exiting Keyword")

    def enterRank_specifier(self, ctx:CSharpParser.Rank_specifierContext):
        print("entering Rank Specifier")

    def exitRank_specifier(self, ctx:CSharpParser.Rank_specifierContext):
        print("exiting Rank Specifier")


def get_all_identifiers(tokens):
    identifiers=[]
    if tokens.__len__()<=0:
        return None
    else:
        for token in tokens:
            if token.type==CSharpLexer.IDENTIFIER:
                identifiers.append(token.text)
                print("[IDENTIFIER]:", token.text)
    return identifiers



if __name__ == '__main__':
    # 直接通过路径读取
    # path="C:\\Users\\Eric.Apollo\\Desktop\\App.xaml.cs"
    path = "C:\\Users\\Administrator\\Desktop\\App.xaml.cs"



    # 读取文件内容
    file_bytes = open(path,"rb").read()

    # 查看文件编码
    encode = (chardet.detect(file_bytes))["encoding"] \
        if (chardet.detect(file_bytes))["encoding"] is not None \
        else "utf-8"

    # 按照文件编码获取输入流
    input_stream = FileStream(path,encoding=encode)

    """
    通过python 使用antlr4 对C# 代码进行解析主要分为三步
    1. Lexer 词法分析
    2. CSharpPreprocessorParser 预解析
    3. CSharpParser 解析
    """

    # 新建词法分析机器
    lexer = CSharpLexer(input_stream)
    # 获取分词结果
    tokens=lexer.getAllTokens()

    # 分词结果流
    directive_token_stream=CommonTokenStream(lexer)
    # 预解析器
    preprocessor_parser=CSharpPreprocessorParser(directive_token_stream)
    # 监听器（目前暂时还未使用）
    listener= preprocessor_parser.getParseListeners()
    index = 0
    # TODO：添加注释
    compiled_tokens = True
    # 注释型token列表
    comment_tokens=[]
    # 指令型token列表
    directive_tokens=[]
    # 代码型token列表
    code_tokens=[]

    # while index < tokens.__len__():
    #     token = tokens[index]
    #     if token.type==CSharpLexer.USING:
    #         print("[USING]:",token.text)
    #     if token.type==CSharpLexer.NAMESPACE:
    #         print("[NAMESPACE]:",token.text)
    #     if token.type==CSharpLexer.ASSIGNMENT:
    #         print("[ASSIGNMENT]:", token.text)
    #     if token.type==CSharpLexer.CLASS:
    #         print("[CLASS]:", token.text)
    #     if token.channel==CSharpLexer.DIRECTIVE:
    #         print("[DIRECTIVE]:", token.text)
    #     if token.type==CSharpLexer.DIRECTIVE_HIDDEN:
    #         print("[DIRECTIVE_HIDDEN]:", token.text)
    #     if token.type==CSharpLexer.IDENTIFIER:
    #         print("[IDENTIFIER]:", token.text)
    #     index=index+1

    index=0
    while index < tokens.__len__():
        token = tokens[index]

        if token.type == CSharpLexer.SHARP:
            tokens.clear()
            directiveTokenIndex = index + 1

            # Collect all preprocessor directive tokens.
            while (directiveTokenIndex < tokens.__len__() and
                   tokens[directiveTokenIndex].type != CSharpLexer.TYPEOF and
                   tokens[directiveTokenIndex].type != CSharpLexer.DIRECTIVE_NEW_LINE and
                   tokens[directiveTokenIndex].type != CSharpLexer.SHARP):

                if tokens[directiveTokenIndex].Channel == CSharpLexer.COMMENTS_CHANNEL:
                    comment_tokens.append(tokens[directiveTokenIndex])
                elif tokens[directiveTokenIndex].Channel != Lexer.HIDDEN:
                    directive_tokens.append(tokens[directiveTokenIndex])

                directiveTokenIndex = directiveTokenIndex + 1

                directiveTokenSource = ListTokenSource(directive_tokens)
                directiveTokenStream = CommonTokenStream(directiveTokenSource, CSharpLexer.DIRECTIVE)
                preprocessor_parser.setInputStream(directiveTokenStream)
                preprocessor_parser.reset()
                # Parse condition in preprocessor directive(based on CSharpPreprocessorParser.g4 grammar).
                directive = preprocessor_parser.preprocessor_directive()

                # if true than next code is valid and not ignored.
                compiled_tokens = directive.value
                directiveStr = tokens.get(index + 1).getText().trim()
                if directiveStr in ["line","error","warning","define","endregion","endif","pragma"]:
                    compiled_tokens = True

                conditionalSymbol = None
                if "define"==tokens.get(index + 1).getText():
                    conditionalSymbol = tokens.get(index + 2).getText()
                    preprocessor_parser.ConditionalSymbols.add(conditionalSymbol)
                if "undef"==tokens.get(index + 1).getText():
                    conditionalSymbol = tokens.get(index + 2).getText()
                    preprocessor_parser.ConditionalSymbols.remove(conditionalSymbol)

                index = directiveTokenIndex - 1

        elif token.channel == lexer.COMMENTS_CHANNEL:
            # 当前token是注释
            comment_tokens.append(token)

        elif token.channel != lexer.HIDDEN and token.type != CSharpLexer.DIRECTIVE_NEW_LINE and compiled_tokens:
            # 当前token是代码类型
            code_tokens.append(token)

        index=index+1

    # At second stage tokens parsed in usual way.
    code_token_source = ListTokenSource(code_tokens)
    code_token_stream = CommonTokenStream(code_token_source)
    parser = CSharpParser(code_token_stream)

    identifiers=get_all_identifiers(tokens)
    # Parse syntax tree(CSharpParser.g4)

    # compilationUnit = parser.compilation_unit()

    # 使用监听器机制遍历
    # listener=MyListener()
    # walker=ParseTreeWalker()
    # walker.walk(listener,compilationUnit)

    # 使用访问者机制遍历
    # vistor=MbParserVistor()
    # vistor.visit(compilationUnit)


    # printer=KeyPrinter()
    # walker=ParseTreeWalker()
    # walker.walk(printer,compilationUnit)
    print("ll")

    # 开启虚拟机
    # startJVM('C:\\Program Files\\Java\\jre1.8.0_91\\bin\\server\\jvm.dll')
    # startJVM(getDefaultJVMPath())
    # 关闭JVM
    # shutdownJVM()

    # if token.type==CSharpLexer.USING:
    #     print("[USING]:",token.text)
    # if token.type==CSharpLexer.NAMESPACE:
    #     print("[NAMESPACE]:",token.text)
    # if token.type==CSharpLexer.ASSIGNMENT:
    #     print("[ASSIGNMENT]:", token.text)
    # if token.type==CSharpLexer.CLASS:
    #     print("[CLASS]:", token.text)
    # if token.channel==CSharpLexer.DIRECTIVE:
    #     print("[DIRECTIVE]:", token.text)
    # if token.type==CSharpLexer.DIRECTIVE_HIDDEN:
    #     print("[DIRECTIVE_HIDDEN]:", token.text)