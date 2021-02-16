import sys
from antlr4 import *
from PolyLexer import PolyLexer
from PolyParser import PolyParser
from TreeVisitor import TreeVisitor


class Interpret():

    def __init__(self):
        self.visitor = TreeVisitor()

    # Envia l'input al lexer i al parser per obtenir l'arbre, i envia l'arbre al TreeVisitor
    def executarInstruccio(self, instruccio):

        input_stream = InputStream(instruccio)

        lexer = PolyLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = PolyParser(token_stream)
        tree = parser.root()

        # print(tree.toStringTree(recog=parser))

        result = self.visitor.visit(tree)
        return result
