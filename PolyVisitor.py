# Generated from Poly.g by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .PolyParser import PolyParser
else:
    from PolyParser import PolyParser

# This class defines a complete generic visitor for a parse tree produced by PolyParser.

class PolyVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by PolyParser#root.
    def visitRoot(self, ctx:PolyParser.RootContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyParser#linea.
    def visitLinea(self, ctx:PolyParser.LineaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyParser#comentari.
    def visitComentari(self, ctx:PolyParser.ComentariContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyParser#text.
    def visitText(self, ctx:PolyParser.TextContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyParser#crea.
    def visitCrea(self, ctx:PolyParser.CreaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyParser#poligon.
    def visitPoligon(self, ctx:PolyParser.PoligonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyParser#capsa.
    def visitCapsa(self, ctx:PolyParser.CapsaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyParser#random.
    def visitRandom(self, ctx:PolyParser.RandomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyParser#parentesi.
    def visitParentesi(self, ctx:PolyParser.ParentesiContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyParser#vertex.
    def visitVertex(self, ctx:PolyParser.VertexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyParser#point.
    def visitPoint(self, ctx:PolyParser.PointContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyParser#nom.
    def visitNom(self, ctx:PolyParser.NomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyParser#consulta.
    def visitConsulta(self, ctx:PolyParser.ConsultaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyParser#contingut.
    def visitContingut(self, ctx:PolyParser.ContingutContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyParser#rgb.
    def visitRgb(self, ctx:PolyParser.RgbContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyParser#imatge.
    def visitImatge(self, ctx:PolyParser.ImatgeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyParser#anychar.
    def visitAnychar(self, ctx:PolyParser.AnycharContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyParser#character.
    def visitCharacter(self, ctx:PolyParser.CharacterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PolyParser#num.
    def visitNum(self, ctx:PolyParser.NumContext):
        return self.visitChildren(ctx)



del PolyParser