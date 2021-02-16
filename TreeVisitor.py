import sys
from polygon import *

if __name__ is not None and "." in __name__:
    from .PolyParser import PolyParser
    from .PolyVisitor import PolyVisitor
else:
    from PolyParser import PolyParser
    from PolyVisitor import PolyVisitor


class TreeVisitor(PolyVisitor):

    def __init__(self):
        self.nivell = 0
        self.imatgesRoot = 'Imatges/'
        self.file = self.imatgesRoot + 'imatge.png'

    def visitRoot(self, ctx: PolyParser.RootContext):
        fills = [n for n in ctx.getChildren()]
        missatge = []
        for x in fills:
            missatge.append(self.visit(x))
        return missatge

    def visitLinea(self, ctx: PolyParser.LineaContext):
        fills = [n for n in ctx.getChildren()]
        if (PolyParser.ruleNames[fills[0].getRuleIndex()] != "comentari"):
            return self.visit(fills[0])

    def visitCrea(self, ctx: PolyParser.CreaContext):
        fills = [n for n in ctx.getChildren()]
        nom = self.visit(fills[0])
        troba = Polygon.getPoly(nom)
        if (isinstance(troba, str)):
            aux = self.visit(fills[2])
            aux.setNom(nom)
        else:
            col = troba.getColor()
            troba.setVertices((self.visit(fills[2])).getVertices())
            troba.setColor(col)

    def visitPoligon(self, ctx: PolyParser.PoligonContext):
        fills = [n for n in ctx.getChildren()]
        if len(fills) == 1:
            if (PolyParser.ruleNames[fills[0].getRuleIndex()] == 'nom'):
                return Polygon.getPoly(self.visit(fills[0]))
            else:
                return self.visit(fills[0])
        else:
            if (PolyParser.symbolicNames[fills[1].getSymbol().type] == 'UNION'):
                return union(self.visit(fills[0]), self.visit(fills[2]))
            else:
                return intersection(self.visit(fills[0]), self.visit(fills[2]))

    def visitRandom(self, ctx: PolyParser.RandomContext):
        fills = [n for n in ctx.getChildren()]
        return genRandomPoly(int(fills[1].getText()))

    def visitParentesi(self, ctx: PolyParser.ParentesiContext):
        fills = [n for n in ctx.getChildren()]
        return self.visit(fills[1])

    def visitCapsa(self, ctx: PolyParser.CapsaContext):
        fills = [n for n in ctx.getChildren()]
        return (self.visit(fills[1])).boundingBox()

    def visitVertex(self, ctx: PolyParser.VertexContext):
        fills = [n for n in ctx.getChildren()]
        punts = []
        for x in range(1, len(fills)-1):
            punts.append(self.visit(fills[x]))
        p = Polygon(punts)
        # p.showVertices()
        return p

    def visitPoint(self, ctx: PolyParser.PointContext):
        fills = [n for n in ctx.getChildren()]
        a = float(fills[0].getText())
        b = float(fills[1].getText())
        return (a, b)

    def visitNom(self, ctx: PolyParser.NomContext):
        return ctx.getText()

    def visitConsulta(self, ctx: PolyParser.ConsultaContext):
        fills = [n for n in ctx.getChildren()]
        if (PolyParser.symbolicNames[fills[0].getSymbol().type] == 'COLOR'):
            (self.visit(fills[1])).setColor(self.visit(fills[3]))
        elif (PolyParser.symbolicNames[fills[0].getSymbol().type] == 'PINTA'):
            if (PolyParser.ruleNames[fills[1].getRuleIndex()] == 'contingut'):
                return self.visit(fills[1])
            else:
                return (self.visit(fills[1])).showVertices()
        elif (PolyParser.symbolicNames[fills[0].getSymbol().type] == 'AREA'):
            return (self.visit(fills[1])).areaPoly()
        elif (PolyParser.symbolicNames[fills[0].getSymbol().type] == 'PERIMITER'):
            return (self.visit(fills[1])).perimiterLength()
        elif (PolyParser.symbolicNames[fills[0].getSymbol().type] == 'VERTICES'):
            return str((self.visit(fills[1])).getNumVertices())
        elif (PolyParser.symbolicNames[fills[0].getSymbol().type] == 'CENTROID'):
            return (self.visit(fills[1])).getCentroid()
        elif (PolyParser.symbolicNames[fills[0].getSymbol().type] == 'EQUAL'):
            return equalPoly(self.visit(fills[1]), self.visit(fills[3]))
        elif (PolyParser.symbolicNames[fills[0].getSymbol().type] == 'INSIDE'):
            return (self.visit(fills[3])).polyInPoly(self.visit(fills[1]))

    def visitContingut(self, ctx: PolyParser.ContingutContext):
        fills = [n for n in ctx.getChildren()]
        return fills[1].getText()

    def visitRgb(self, ctx: PolyParser.RgbContext):
        fills = [n for n in ctx.getChildren()]
        r = int(255*float(fills[1].getText()))
        g = int(255*float(fills[2].getText()))
        b = int(255*float(fills[3].getText()))
        return [r, g, b]

    def visitImatge(self, ctx: PolyParser.ImatgeContext):
        fills = [n for n in ctx.getChildren()]
        filename = fills[2].getText()
        polys = []
        for x in range(5, len(fills), 2):
            if (PolyParser.ruleNames[fills[x].getRuleIndex()] == 'poligon'):
                polys.append(self.visit(fills[x]))
        r = drawPolygons(polys, filename)
        return r
