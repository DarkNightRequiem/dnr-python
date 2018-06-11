import sys
from antlr4 import *
from antlr4.ListTokenSource import ListTokenSource
from jpype import *
from util.antlr4.recognizers.CSharpLexer import CSharpLexer
from util.antlr4.recognizers.CSharpParser import CSharpParser
from util.antlr4.recognizers.CSharpParserListener import CSharpParserListener
from util.antlr4.recognizers.CSharpPreprocessorParser import CSharpPreprocessorParser

class KeyPrinter(CSharpParserListener):
    def exitKey(self, ctx):
        print("Oh, a key!")


if __name__ == '__main__':
    # 直接通过路径读取
    # path="C:\\Users\\Eric.Apollo\\Desktop\\App.xaml.cs"
    path = "C:\\Users\\Administrator\\Desktop\\App.xaml.cs"
    input_stream = FileStream(path,encoding='utf-8')

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

    while index < tokens.__len__():
        token = tokens[index]
        if token.type == CSharpLexer.SHARP:
            tokens.clear()
            directiveTokenIndex = index + 1

            # Collect all preprocessor directive tokens.
            while (directiveTokenIndex < tokens.Count and tokens[directiveTokenIndex].Type != CSharpLexer.TYPEOF and
                   tokens[directiveTokenIndex].Type != CSharpLexer.DIRECTIVE_NEW_LINE and tokens[directiveTokenIndex].Type != CSharpLexer.SHARP):

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
                index = directiveTokenIndex - 1

        elif token.Channel == lexer.COMMENTS_CHANNEL:
            # 当前token是注释
            comment_tokens.append(token)
        elif token.Channel != Lexer.HIDDEN and token.Type != CSharpLexer.DIRECTIVE_NEW_LINE and compiled_tokens:
            # 当前token是代码类型
            code_tokens.append(token)

        index=index+1

    # At second stage tokens parsed in usual way.
    codeTokenSource = ListTokenSource(tokens)
    codeTokenStream = CommonTokenStream(codeTokenSource)
    parser = CSharpParser(codeTokenStream)

    # Parse syntax tree(CSharpParser.g4)
    compilationUnit = parser.compilation_unit()

    print("ll")

    # 开启虚拟机
    # startJVM('C:\\Program Files\\Java\\jre1.8.0_91\\bin\\server\\jvm.dll')
    # startJVM(getDefaultJVMPath())
    # 关闭JVM
    # shutdownJVM()