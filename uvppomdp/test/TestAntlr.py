import sys
from antlr4 import *
from jpype import *
from util.antlr4.recognizers.CSharpLexer import CSharpLexer
# from util.antlr4.recognizers.CSharpParser import CSharpParser
# from util.antlr4.recognizers.CSharpParserListener import CSharpParserListener


# class KeyPrinter(CSharpParserListener):
#     def exitKey(self, ctx):
#         print("Oh, a key!")


if __name__ == '__main__':
    # 直接通过路径读取
    # path="C:\\Users\\Eric.Apollo\\Desktop\\App.xaml.cs"
    # input_stream=FileStream(path)

    # 开启虚拟机
    # startJVM('C:\\Program Files\\Java\\jre1.8.0_91\\bin\\server\\jvm.dll')
    startJVM(getDefaultJVMPath())

    # lexer=CSharpLexer(input_stream)
    # stream=CommonTokenStream(lexer)

    # parser=CSharpParser(stream)
    #
    # tree = parser.buildParseTrees()
    # printer=KeyPrinter()
    #
    # walker=ParseTreeWalker()
    # walker.walk(printer, tree)

    # 关闭JVM
    shutdownJVM()


    print("ll")

    # 通过压缩包读取
    # TODO: 实现