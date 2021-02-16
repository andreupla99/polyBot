import math
import random
from PIL import Image


# Retorna la distància entre dos punts
def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x2-x1)**2+(y2-y1)**2)


# Retorna l'àrea que forma el triangle donats tres punts
def areaTriangle(p1, p2, p3):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    a = (x1*y2+x2*y3+x3*y1-y1*x2-y2*x3-y3*x1)/2
    if a < 0:
        a = -a
    return a


# Retorna el vector entre dos punts
def pointsToVec(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    r = (x2-x1, y2-y1)
    return r


# Retorna l'angle format per dos vectors entre tres punts
def getAngle(a, b, c):
    bc = pointsToVec(b, c)
    ba = pointsToVec(b, a)
    x1, y1 = bc
    x2, y2 = ba
    r = math.atan2(y1, x1) - math.atan2(y2, x2)
    r *= 180/math.pi
    if (r < 0):
        r += 360
    return r


# Retorna els la posició dels punts que formen vectors incidents (on creuen arestes)
def findIntersectingVertices(poly1, poly2, inner):
    start = 0
    end = 0

    if (poly2.pointInPoly(poly1.getVertices()[0])):
        for x in range(1, poly1.getNumVertices()):
            if (not poly2.pointInPoly(poly1.getVertices()[x])):
                if inner:
                    end = x-1
                else:
                    start = x
                break
            if x == poly1.getNumVertices()-1:
                return (-1, -1)
        if inner:
            start = end+2
            if (start == poly1.getNumVertices()):
                start = 0
            while (start != end):
                if (poly2.pointInPoly(poly1.getVertices()[start])):
                    break
                start += 1
                if start == poly1.getNumVertices():
                    start = 0
        else:
            end = start+1
            if (end == poly1.getNumVertices()):
                end = 0
            while (end != start):
                if (poly2.pointInPoly(poly1.getVertices()[end])):
                    if (end == 0):
                        end = poly1.getNumVertices()-1
                    else:
                        end -= 1
                    break
                end += 1
                if end == poly1.getNumVertices():
                    end = 0
    else:
        for x in range(1, poly1.getNumVertices()):
            if (poly2.pointInPoly(poly1.getVertices()[x])):
                if inner:
                    start = x
                else:
                    end = x-1
                break
            if x == poly1.getNumVertices()-1:
                return (-1, -1)
        if inner:
            if start == poly1.getNumVertices()-1:
                end = 0
            else:
                end = start+1
            while (end != start):
                if (not poly2.pointInPoly(poly1.getVertices()[end])):
                    if end == 0:
                        end = poly1.getNumVertices()-1
                    else:
                        end = end-1
                    break
                end += 1
                if end == poly1.getNumVertices():
                    end = 0
        else:
            if end == poly1.getNumVertices()-1:
                start = 0
            else:
                start = end+1
            while (start != end):
                if (not poly2.pointInPoly(poly1.getVertices()[start])):
                    break
                start += 1
                if start == poly1.getNumVertices():
                    start = 0

    return (start, end)


# Retorna el punt d'interseccio entre dos vectors
def findIntersectionPoint(pa, pc, vab, vcd):
    xa, ya = pa
    xc, yc = pc
    xab, yab = vab
    xcd, ycd = vcd
    if (ycd*xab-yab*xcd) == 0:
        return pa
    t2 = (((ya-yc)*xab)+yab*(xc-xa))/(ycd*xab-yab*xcd)
    x = xc+xcd*t2
    y = yc+ycd*t2
    return (x, y)


# Retorna el polígon corresponent a la intersecció de dos polígons convexos
def intersection(poly1, poly2):
    if (poly1.polyInPoly(poly2) == 'yes'):
        return poly2
    if (poly2.polyInPoly(poly1) == 'yes'):
        return poly1
    s1, e1 = findIntersectingVertices(poly1, poly2, True)
    s2, e2 = findIntersectingVertices(poly2, poly1, True)
    if (poly1.getVertices()[s1] == poly2.getVertices()[e2] and poly2.getVertices()[s2] == poly1.getVertices()[e1]):
        x1, y1 = poly1.getVertices()[s1]
        x2, y2 = poly1.getVertices()[e1]
        if (x1 < x2 or (x1 == x2 and y1 < y2)):
            resV = [poly1.getVertices()[s1], poly1.getVertices()[e1]]
        else:
            resV = [poly1.getVertices()[e1], poly1.getVertices()[s1]]
        ret = Polygon(resV)
        return ret
    if poly1.getVertices()[s1] == poly2.getVertices()[e2]:
        resV = [poly1.getVertices()[s1]]
        if (e2 == 0):
            e2 = poly2.getNumVertices()-1
        else:
            e2 -= 1
        if (s1 == poly1.getNumVertices()-1):
            s1 = 0
        else:
            s1 += 1
    else:
        if s1 == 0:
            ab = pointsToVec(poly1.getVertices()[poly1.getNumVertices()-1], poly1.getVertices()[s1])
        else:
            ab = pointsToVec(poly1.getVertices()[s1-1], poly1.getVertices()[s1])

        if e2 == poly2.getNumVertices()-1:
            cd = pointsToVec(poly2.getVertices()[e2], poly2.getVertices()[0])
        else:
            cd = pointsToVec(poly2.getVertices()[e2], poly2.getVertices()[e2+1])

        if s1 == 0:
            resV = [findIntersectionPoint(poly1.getVertices()[poly1.getNumVertices()-1], poly2.getVertices()[e2], ab, cd)]
        else:
            resV = [findIntersectionPoint(poly1.getVertices()[s1-1], poly2.getVertices()[e2], ab, cd)]

    while s1 != e1:
        resV.append(poly1.getVertices()[s1])
        s1 += 1
        if (s1 == poly1.getNumVertices()):
            s1 = 0

    resV.append(poly1.getVertices()[e1])

    if poly2.getVertices()[s2] == poly1.getVertices()[e1]:
        resV.append(poly2.getVertices()[s2])
        if (s2 == poly2.getNumVertices()-1):
            s2 = 0
        else:
            s2 += 1
    else:
        if s2 == 0:
            ab = pointsToVec(poly2.getVertices()[poly2.getNumVertices()-1], poly2.getVertices()[s2])
        else:
            ab = pointsToVec(poly2.getVertices()[s2-1], poly2.getVertices()[s2])

        if e1 == poly1.getNumVertices()-1:
            cd = pointsToVec(poly1.getVertices()[e1], poly1.getVertices()[0])
        else:
            cd = pointsToVec(poly1.getVertices()[e1], poly1.getVertices()[e1+1])

        if s2 == 0:
            resV.append(findIntersectionPoint(poly2.getVertices()[poly2.getNumVertices()-1], poly1.getVertices()[e1], ab, cd))
        else:
            resV.append(findIntersectionPoint(poly2.getVertices()[s2-1], poly1.getVertices()[e1], ab, cd))

    while s2 != e2:
        resV.append(poly2.getVertices()[s2])
        s2 += 1
        if (s2 == poly2.getNumVertices()):
            s2 = 0

    resV.append(poly2.getVertices()[e2])
    ret = Polygon(resV)
    return ret


# Retorna la unió convexa de dos polígons convexos
def union(poly1, poly2):
    if (poly1.polyInPoly(poly2) == 'yes'):
        return poly1
    if (poly2.polyInPoly(poly1) == 'yes'):
        return poly2
    s1, e1 = findIntersectingVertices(poly1, poly2, False)
    s2, e2 = findIntersectingVertices(poly2, poly1, False)
    if poly1.getVertices()[s1] == poly2.getVertices()[e2]:
        resV = [poly1.getVertices()[s1]]
        if (e2 == 0):
            e2 = poly2.getNumVertices()-1
        else:
            e2 -= 1
        if (s1 == poly1.getNumVertices()-1):
            s1 = 0
        else:
            s1 += 1
    else:
        if s1 == 0:
            ab = pointsToVec(poly1.getVertices()[poly1.getNumVertices()-1], poly1.getVertices()[s1])
        else:
            ab = pointsToVec(poly1.getVertices()[s1-1], poly1.getVertices()[s1])

        if e2 == poly2.getNumVertices()-1:
            cd = pointsToVec(poly2.getVertices()[e2], poly2.getVertices()[0])
        else:
            cd = pointsToVec(poly2.getVertices()[e2], poly2.getVertices()[e2+1])

        if s1 == 0:
            resV = [findIntersectionPoint(poly1.getVertices()[poly1.getNumVertices()-1], poly2.getVertices()[e2], ab, cd)]
        else:
            resV = [findIntersectionPoint(poly1.getVertices()[s1-1], poly2.getVertices()[e2], ab, cd)]

    while s1 != e1:
        resV.append(poly1.getVertices()[s1])
        s1 += 1
        if (s1 == poly1.getNumVertices()):
            s1 = 0

    resV.append(poly1.getVertices()[e1])

    if poly2.getVertices()[s2] == poly1.getVertices()[e1]:
        resV.append(poly2.getVertices()[s2])
        if (s2 == poly2.getNumVertices()-1):
            s2 = 0
        else:
            s2 += 1
    else:
        if s2 == 0:
            ab = pointsToVec(poly2.getVertices()[poly2.getNumVertices()-1], poly2.getVertices()[s2])
        else:
            ab = pointsToVec(poly2.getVertices()[s2-1], poly2.getVertices()[s2])

        if e1 == poly1.getNumVertices()-1:
            cd = pointsToVec(poly1.getVertices()[e1], poly1.getVertices()[0])
        else:
            cd = pointsToVec(poly1.getVertices()[e1], poly1.getVertices()[e1+1])

        if s2 == 0:
            resV.append(findIntersectionPoint(poly2.getVertices()[poly2.getNumVertices()-1], poly1.getVertices()[e1], ab, cd))
        else:
            resV.append(findIntersectionPoint(poly2.getVertices()[s2-1], poly1.getVertices()[e1], ab, cd))

    while s2 != e2:
        resV.append(poly2.getVertices()[s2])
        s2 += 1
        if (s2 == poly2.getNumVertices()):
            s2 = 0

    resV.append(poly2.getVertices()[e2])
    ret = Polygon(resV)
    ret.makeConvex()
    return ret


# Modifica un píxel de l'arxiu .png donat a "imatge"
def drawPixel(image, x, y, color):
    pixels = image.load()
    x += 1
    y += 1
    if (x >= 0 and y >= 0 and x < image.size[1] and y < image.size[0]):
        pixels[x, y] = (color[0], color[1], color[2])


# Pinta un punt amb un radi definit en pixels per width
def drawPoint(image, point, color, width):
    x, y = point
    for i in range(-width, width+1):
        for j in range(-width, width+1):
            drawPixel(image, x+i, y+j, color)


# Pinta una línea a base de pintar punts en el vector entre dos punts
def drawLine(image, pointA, pointB, color):
    x1, y1 = pointA
    x2, y2 = pointB
    aux = x1-x2
    if aux < 0:
        aux = -aux
    d = y1-y2
    if d < 0:
        d = -d
    d += aux
    ab = pointsToVec(pointA, pointB)
    vX, vY = ab
    for i in range(1, d):
        x = int(x1 + (vX * i / d))
        y = int(y1 + (vY * i / d))
        drawPoint(image, (x, y), color, 0)


# Pinta un polígon a base de pintar els vèrtex i les arestes
def drawPolygon(image, poly, widthPolyCoords, hightPolyCoords, realWidth, realHight, minPoint):
    origenX, origenY = minPoint
    newPoints = []
    color = poly.getColor()
    addX = addY = 0
    if realWidth > realHight:
        addY = int((realWidth-realHight)/2)
    else:
        addX = int((realHight-realWidth)/2)
    for x in poly.getVertices():
        realPointX, realPointY = x
        realPointX = int((-(origenX-realPointX)*(realWidth-2))//widthPolyCoords)
        realPointY = int(((origenY-realPointY)*(realHight-2))//hightPolyCoords)
        realPointX += addX
        realPointY += addY
        drawPoint(image, (realPointX, realPointY), color, 1)
        newPoints.append((realPointX, realPointY))

    for x in range(1, len(newPoints)):
        drawLine(image, newPoints[x-1], newPoints[x], color)
    drawLine(image, newPoints[0], newPoints[len(newPoints)-1], color)


# Pinta un llistat de polígons donat a l'arxiu corresponent a "filename"
def drawPolygons(polyList, filename):
    path = "Imatges/"+filename
    algo = False
    minX = minY = maxX = maxY = 0
    for j in polyList:
        for i in range(j.getNumVertices()):
            algo = True
            x, y = j.getVertices()[i]
            if (x < minX):
                minX = x
            else:
                if (x > maxX):
                    maxX = x
            if (y < minY):
                minY = y
            else:
                if (y > maxY):
                    maxY = y

    image = Image.new('RGB', (400, 400), "white")

    if algo:
        widthPolyCoords = maxX-minX
        hightPolyCoords = maxY-minY
        if (widthPolyCoords == 0):
            if (hightPolyCoords == 0):
                widthPolyCoords = 10
                hightPolyCoords = 10
            else:
                widthPolyCoords = hightPolyCoords
        if (hightPolyCoords == 0):
            if (widthPolyCoords != 0):
                hightPolyCoords = widthPolyCoords

        realWidth = 400
        realHight = 400
        if (widthPolyCoords > hightPolyCoords):
            realHight = int(400*hightPolyCoords/widthPolyCoords)
        else:
            realWidth = int(400*widthPolyCoords/hightPolyCoords)

        for x in polyList:
            drawPolygon(image, x, widthPolyCoords, hightPolyCoords, realWidth, realHight, (minX, maxY))

    image.save(path)
    return filename


# Retorna cert si els dos polígons són iguals. Sinó retorna fals
def equalPoly(poly1, poly2):
    if (poly1.polyInPoly(poly2) == 'yes' and poly2.polyInPoly(poly1) == 'yes'):
        return 'yes'
    else:
        return 'no'


# Custom merge sort
def mergeSortVertices(vertexList, origin, reference):
    vList = vertexList
    listSize = len(vList)
    if (listSize < 2):
        return vList
    if (listSize == 2):
        angle1 = getAngle(reference, origin, vList[0])
        angle2 = getAngle(reference, origin, vList[1])
        if (angle1 > angle2):
            return vList
        elif (angle1 == angle2):
            if (distance(origin, vList[0]) > distance(origin, vertexList[1])):
                return [vList[0]]
            else:
                return [vList[1]]
        else:
            return [vList[1], vList[0]]
    else:
        mid = int(listSize/2)
        l1 = mergeSortVertices(vList[0: mid+1], origin, reference)
        if (mid+1 == listSize-1):
            l2 = [vList[listSize-1]]
        else:
            l2 = mergeSortVertices(vList[mid+1: listSize], origin, reference)
        outList = []
        while (len(l1) > 0 or len(l2) > 0):
            if (len(l1) == 0):
                outList.extend(l2)
                return outList
            elif (len(l2) == 0):
                outList.extend(l1)
                return outList
            else:
                angle1 = getAngle(reference, origin, l1[0])
                angle2 = getAngle(reference, origin, l2[0])
                if (angle1 > angle2):
                    outList.append(l1[0])
                    l1.pop(0)
                elif (angle1 < angle2):
                    outList.append(l2[0])
                    l2.pop(0)
                else:
                    if (distance(origin, l1[0]) > distance(origin, l2[0])):
                        outList.append(l1[0])
                        l1.pop(0)
                        l2.pop(0)
                    else:
                        outList.append(l2[0])
                        l1.pop(0)
                        l2.pop(0)
        return outList


# retorna un polígon amb "num" o menys vèrtex generats aleatòriament
def genRandomPoly(num):
    points = []
    for x in range(num):
        # establim 5 decimals de precisió perquè no siguin massa complexos d'operar
        points.append((float(format(random.random(), ".5f")), float(format(random.random(), ".5f"))))
        # si volem tots els decimals cal substituir-lo per la següent línea
        # points.append(random.random(),random.random())
    ret = Polygon(points)
    return ret


# Classe principal, les estructures de dades i com tractarles.
class Polygon:

    polygons = []

    def __init__(self, vertices):
        self.vertices = vertices
        self.nom = ""
        self.color = [0, 0, 0]
        self.numVertex = len(vertices)
        if (self.numVertex >= 3 and not self.checkConvex()):
            self.correctCoords()

    # Retorna el llistat de vèrtex del polígon
    def getVertices(self):
        return self.vertices

    # Retorna el nombre de vèrtex del polígon
    def getNumVertices(self):
        return self.numVertex

    # Retorna el nombre d'arestes del polígon
    def getNumEdges(self):
        if self.numVertex < 3:
            return self.numVertex-1
        return self.numVertex

    # Estableix el llistat de vèrtex del polígon al que conté vert
    def setVertices(self, vert):
        self.vertices = vert

    # Retorna el color del polígon
    def getColor(self):
        return self.color

    # Retorna el nom del polígon
    def getNom(self):
        return self.nom

    # Estableix el color del polígon
    def setColor(self, rgb):
        self.color = rgb

    # Estableix el nom del polígon, si no tenia nom l'afegeix al llistat de polígons amb nom "polygons"
    def setNom(self, nom):
        if nom != "":
            if self.nom == "":
                self.nom = nom
                Polygon.polygons.append(self)
            else:
                self.nom = nom

    # Comprova si el poligon es convex
    def checkConvex(self):
        if (self.numVertex < 3) and (self.numVertex > 0):
            return False
        elif getAngle(self.vertices[self.numVertex-2], self.vertices[self.numVertex-1], self.vertices[0]) > 180:
            return False
        elif getAngle(self.vertices[self.numVertex-1], self.vertices[0], self.vertices[1]) > 180:
            return False
        else:
            for x in range(2, self.numVertex):
                if getAngle(self.vertices[x-2], self.vertices[x-1], self.vertices[x]) > 180:
                    return False
        if (x == self.numVertex-1 and not getAngle(self.vertices[x-2], self.vertices[x-1], self.vertices[x]) > 180):
            return True

    # Comprova si el punt "point" està al polígon
    def pointInPoly(self, point):
        if (point in self.vertices):
            return True
        if getAngle(point, self.vertices[self.numVertex-1], self.vertices[0]) > 180:
            return False
        for x in range(1, self.numVertex):
            if point == self.vertices[x-1] or point == self.vertices[x]:
                return True
            if getAngle(point, self.vertices[x-1], self.vertices[x]) > 180:
                return False
        return True

    # Comprova si el poligon "polygon" està dins del polígon
    def polyInPoly(self, polygon):
        if polygon == self:
            return 'yes'
        for x in polygon.getVertices():
            if not self.pointInPoly(x):
                return 'no'
        return 'yes'

    # Retorna el perímetre del polígon
    def perimiterLength(self):
        r = distance(self.vertices[self.numVertex-1], self.vertices[0])
        for x in range(1, self.numVertex):
            r += distance(self.vertices[x-1], self.vertices[x])
        return str(format(float(r), ".3f"))

    # Retorna l'àrea del polígon
    def areaPoly(self):
        a = 0
        for x in range(2, self.numVertex):
            a += areaTriangle(self.vertices[0], self.vertices[x-1], self.vertices[x])
        return str(format(float(a), ".3f"))

    # Retorna el centroide del polígon
    def getCentroid(self):
        x1, y1 = self.vertices[self.numVertex-1]
        x2, y2 = self.vertices[0]
        det = x1*y2-x2*y1
        cx = (x1+x2)*det
        cy = (y1+y2)*det
        for x in range(1, self.numVertex):
            x1, y1 = self.vertices[x-1]
            x2, y2 = self.vertices[x]
            tempDet = x1*y2-x2*y1
            det += tempDet
            cx += (x1+x2)*tempDet
            cy += (y1+y2)*tempDet
        cx /= 3*det
        cy /= 3*det
        return str(format(float(cx), ".3f"))+" "+str(format(float(cy), ".3f"))

    # Comprova si el polígon és regular
    def checkRegular(self):
        if not self.checkConvex():
            return False
        dist = distance(self.vertices[self.numVertex-1], self.vertices[0])
        for x in range(1, self.numVertex):
            if (distance(self.vertices[x-1], self.vertices[x]) != dist):
                return False
        return True

    # Retorna els vèrtex del polígon en forma de string
    def showVertices(self):
        out = ""
        for x in self.vertices:
            a, b = x
            out += str(format(float(a), ".3f"))+" "+str(format(float(b), ".3f"))
            if (x != self.vertices[self.getNumVertices()-1]):
                out += " "
        return out

    # Retorna el polígon corresponent a la capsa contenidora del polígon
    def boundingBox(self):
        minX = minY = maxX = maxY = 0
        for i in range(self.numVertex):
            x, y = self.vertices[i]
            if (x < minX):
                minX = x
            else:
                if (x > maxX):
                    maxX = x
            if (y < minY):
                minY = y
            else:
                if (y > maxY):
                    maxY = y
        r = [(minX, minY), (minX, maxY), (maxX, maxY), (maxX, minY)]
        ret = Polygon(r)
        return ret

    # Converteix el polígon en un polígon convex
    def makeConvex(self):
        convex = False
        while (not convex):
            convex = True
            x = 0
            while (x < self.numVertex):
                if (x == 0):
                    if (getAngle(self.vertices[self.numVertex-1], self.vertices[x], self.vertices[x+1]) > 180):
                        self.vertices.pop(x)
                        x -= 1
                        self.numVertex -= 1
                        convex = False
                else:
                    if (x == self.numVertex-1):
                        if (getAngle(self.vertices[x-1], self.vertices[x], self.vertices[0]) > 180):
                            self.vertices.pop(x)
                            x -= 1
                            self.numVertex -= 1
                            convex = False
                    else:
                        if (getAngle(self.vertices[x-1], self.vertices[x], self.vertices[x+1]) > 180):
                            self.vertices.pop(x)
                            x -= 1
                            self.numVertex -= 1
                            convex = False
                x += 1

    # Selecciona els punts adientment per tal de poder formar un polígon convex
    def correctCoords(self):
        minX, minY = self.vertices[0]
        for x in range(1, self.numVertex):
            a, b = self.vertices[x]
            if a < minX:
                minX = a
                minY = b
            else:
                if a == minX:
                    if b < minY:
                        minX = a
                        minY = b
        self.vertices.remove((minX, minY))
        refX = minX
        refY = minY-1
        self.vertices = mergeSortVertices(self.vertices, (minX, minY), (refX, refY))
        self.vertices.insert(0, (minX, minY))
        self.numVertex = len(self.vertices)
        if (self.numVertex >= 3):
            self.makeConvex()

    # Retorna el polígon amb nom "nom" guardat a "polygon", si no existeix retorna error
    def getPoly(nom):
        for x in Polygon.polygons:
            if nom == x.getNom():
                return x
        return "Error: Could not find polygon \"" + nom + "\""
