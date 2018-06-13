# --------------------------------------------
# @File     : MbParserVistor.py
# @Time     : 2018/6/12 20:11
# @Author   : Yanqing Wang (DarkNightRequiem)
# @Note     : This File is currently not in use
# --------------------------------------------
import chardet
from antlr4 import *
from antlr4.ListTokenSource import ListTokenSource
from util.antlr4.recognizers.CSharpLexer import CSharpLexer
from util.antlr4.recognizers.CSharpParser import CSharpParser
from util.antlr4.recognizers.CSharpParserVisitor import CSharpParserVisitor


class MbParserVistor(CSharpParserVisitor):
    def __init__(self, tokens=[]):
        CSharpParserVisitor.__init__(self)
        self.tokens=tokens

    """""""""""
    重写父类方法
    """""""""""
    def visitNamespace_or_type_name(self, ctx:CSharpParser.Namespace_or_type_nameContext):
        super().visitNamespace_or_type_name(ctx)

    def visitNamespace_declaration(self, ctx:CSharpParser.Namespace_declarationContext):
        namespace= ctx.qi.children[0].symbol.text
        print("[Namespace_declaration]:",namespace)
        super().visitNamespace_declaration(ctx)

    def visitClass_definition(self, ctx:CSharpParser.Class_definitionContext):
        classname= ctx.identifier().children[0].symbol.text
        print("[Class_definition]:", classname)
        super().visitClass_definition(ctx)
    #
    # def visitClass_type(self, ctx:CSharpParser.Class_typeContext):


    def visitClass_body(self, ctx:CSharpParser.Class_bodyContext):
        text=ctx.getText()
        rule_index=ctx.getRuleIndex()
        rule_ctx=ctx.getRuleContext()
        print("[visiting Class_body]:",text)
        super().visitClass_body(ctx)

    def visitAccessor_body(self, ctx:CSharpParser.Accessor_bodyContext):
        text=ctx.getText()
        print("[visiting Accessor_body]:",text)
        super().visitAccessor_body(ctx)

    def visitAccessor_modifier(self, ctx:CSharpParser.Accessor_modifierContext):
        text = ctx.getText()
        print("[visiting Accessor_modifier]:", text)
        super().visitAccessor_modifier(ctx)

    def visitAccessor_declarations(self, ctx:CSharpParser.Accessor_declarationsContext):
        text = ctx.getText()
        print("[visiting visitAccessor_declarations]:", text)
        super().visitAccessor_declarations(ctx)

    def visitNamespace_body(self, ctx:CSharpParser.Namespace_bodyContext):
        text = ctx.getText()
        print("[visiting visitNamespace_body]:", text)
        super().visitNamespace_body(ctx)
