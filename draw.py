import pygame
import pygame.gfxdraw
from maths import *
from fnt import *
from colors import colors


class ContextState:
    color = "white"
    forcedColor = None
    strokeWidth = 2
    matrix: Matrix = Matrix.identity()

    def __init__(self, copy=None, cloneMatrix=True):
        if copy != None:
            self.color = copy.color
            self.forcedColor = copy.forcedColor
            self.strokeWidth = copy.strokeWidth
            if cloneMatrix:
                self.matrix = Matrix.copy(copy.matrix)
            else:
                self.matrix = copy.matrix


class Context:
    _states = []
    surface: any = None
    cull: any = None

    def __init__(self, surface):
        self.surface = surface
        self._states.append(ContextState())

    def save(self):
        self._states.append(ContextState(self.state))

    def saveAttributes(self):
        self._states.append(ContextState(self.state, False))

    def restore(self):
        del self._states[len(self._states) - 1]

    def translate(self, x, y):
        m = Matrix.identity()
        m.translate(x, y, 0)
        self.state.matrix.multiply(m)

    def scale(self, x, y):
        m = Matrix.identity()
        m.scale(x, y, 1)
        self.state.matrix.multiply(m)

    def rotate(self, az):
        m = Matrix.identity()
        m.rotate(0, 0, az * 3.14 / 180)
        self.state.matrix.multiply(m)

    def transform(self, v):
        t = Vector.copy(v)
        return t.transform(self.state.matrix)

    @property
    def state(self):
        return self._states[len(self._states) - 1]

    def clear(self, color):
        self.surface.fill(color)

    def _drawLine(self, v1, v2, color=None):
        if isinstance(color, str):
            clrs = color.title()
            clrs1 = clrs + "1"
            clrs2 = clrs + "2"
            clrs3 = clrs + "3"
            if clrs in colors:
                color = colors[clrs]
            elif clrs3 in colors:
                color = colors[clrs3]
            elif clrs2 in colors:
                color = colors[clrs2]
            elif clrs1 in colors:
                color = colors[clrs1]
            else:
                print(color)
                color = [255, 255, 255]

        w = self.state.strokeWidth
        if w == 1:
            pygame.gfxdraw.line(
                self.surface, Floor(v1.x), Floor(v1.y), Floor(v2.x), Floor(v2.y), color
            )

        d = Vector.copy(v2).subtract(v1).normalize()
        sideDir = Vector(0, 0, 1).cross(d).scale(w * 0.48)
        v3 = Vector.copy(v1).add(sideDir)
        v4 = Vector.copy(v2).add(sideDir)
        v1.subtract(sideDir)
        v2.subtract(sideDir)

        pygame.gfxdraw.filled_polygon(
            self.surface,
            [
                [(v1.x), (v1.y)],
                [(v3.x), (v3.y)],
                [(v4.x), (v4.y)],
                [(v2.x), (v2.y)],
            ],
            color,
        )

    def drawLine(self, x, y, x2, y2, color=None):
        if color == None:
            color = self.state.color

        if self.state.forcedColor != None:
            color = self.state.forcedColor

        m = self.state.matrix
        v1 = Vector(x, y).transform(m)
        v2 = Vector(x2, y2).transform(m)

        # add culling
        if self.cull != None:
            if self.cull(v1, v2) == True:
                return

        self._drawLine(v1, v2, color)

        # pygame.draw.line(
        #     self.surface, color, [v1.x, v1.y], [v2.x, v2.y], self.state.strokeWidth
        # )

    def drawRect(self, x, y, w, h, color=None):
        pygame.draw.rect(self.surface, color, [x, y, w, h], self.state.strokeWidth)

    def drawPolygon(self, x, y, r, sides, color=None):
        if sides < 3:
            return

        points = []
        for i in range(0, sides):
            angle = ((360 / sides) * i) * 3.14 / 180
            px = x + r * Cos(angle)
            py = y + r * Sin(angle)
            points.append([px, py])
        points.append(points[0])

        for i in range(1, sides + 1):
            p1 = points[i - 1]
            p2 = points[i]
            self.drawLine(p1[0], p1[1], p2[0], p2[1], color)

    def drawPolygonPoints(self, points, color=None, close=True):
        for i in range(1, len(points) + 1):
            p1 = points[i - 1]
            k = i
            if k == len(points):
                k = 0
                if close == False:
                    break
            p2 = points[k]
            self.drawLine(p1[0], p1[1], p2[0], p2[1], color)

    def drawChar(self, x, y, c, size, color=None, extentsOnly=False):
        pts = fnt[C(c) - C(" ")]
        next_moveto = 1
        startPosition = {}

        adv = x

        for i in range(0, 8):
            delta = pts[i]
            if delta == FONT_LAST:
                break
            if delta == FONT_UP:
                next_moveto = 1
                continue

            dx = ((delta >> 4) & 0xF) * size
            dy = ((delta >> 0) & 0xF) * -size

            if next_moveto != 0:
                startPosition = {"x": x + dx, "y": y + dy}

                if x + dx > adv:
                    adv = x + dx + (size * 4)

            else:
                nextPosition = {"x": x + dx, "y": y + dy}

                if x + dx > adv:
                    adv = x + dx + (size * 4)

                if not extentsOnly:
                    self.drawLine(
                        startPosition["x"],
                        startPosition["y"],
                        nextPosition["x"],
                        nextPosition["y"],
                        color,
                    )

                startPosition = nextPosition

            next_moveto = 0

        adv -= x
        if adv < 12 * size:
            adv = 12 * size

        return adv

    def drawText(self, x, y, text, size, color=None, align=0):
        text = text.upper()

        adv = 0
        extents = 0

        # get extents
        for i in range(0, len(text)):
            c = text[i]
            adv = self.drawChar(x, y, c, size, color, True)
            extents += adv

        # center
        if align == 0:
            x -= extents / 2

        # right
        if align == 2:
            x -= extents

        for i in range(0, len(text)):
            c = text[i]
            adv = self.drawChar(x, y + (-size * 0.5), c, size, color, False)
            x += adv

    def drawShape(self, shapes, x, y, r, angle, color="red", matrix=None):
        sl = shapes
        m = Matrix.fromAngle(angle)
        m.multiply(Matrix.identity().scale(r * 1.5, r * 1.5, 1))
        m.multiply(Matrix.identity().translate(x, y, 0))
        for shape in sl:
            s = shape
            if "points" in s:
                points = []
                p0 = s["points"][0]
                v0 = Vector(p0[0] * r * 15, p0[1] * r * 15)
                for p in s["points"]:
                    tp = Vector(p[0], p[1]).add(v0).transform(m)
                    points.append([tp.x, tp.y])
                del points[0]

                clr = color if not "color" in s else s["color"]
                self.drawPolygonPoints(points, clr)
            if "polygon" in s:
                self.drawPolygon(0, 0, r * s["scale"], s["polygon"], color)
