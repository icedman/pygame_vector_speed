import random
import math


def Rand(s, e):
    s = Floor(s)
    e = Floor(e)
    if e < s:
        return s
    return random.randint(s, e)


def Rnd(s=0, e=0):
    l = e - s
    if l == 0:
        l = 1
    r = random.random() * l
    return s + r


def RndOr(a, b):
    return a if Rand(0, 10) > 5 else b


def Cos(a):
    return math.cos(a)


def Sin(a):
    return math.sin(a)


def Sqr(a):
    return math.sqrt(a)


def Min(a, b):
    return a if a < b else b


def Abs(a):
    return abs(a)


def distance(x, y, x2, y2):
    dx = x - x2
    dy = y - y2
    return math.sqrt((dx * dx) + (dy * dy))


def angleTo(x, y, x2, y2):
    angleRadians = math.atan2(y2 - y, x2 - x)
    angle = angleRadians * 180 / 3.14
    return angle


def Sgn(a):
    if a > 0:
        return 1
    elif a < 0:
        return -1
    return 0


def Floor(a):
    return math.floor(a)


class Matrix:
    M = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    @staticmethod
    def identity():
        m = Matrix()
        m.M = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        return m

    @staticmethod
    def copy(m):
        r = Matrix.identity()
        for row in range(0, 4):
            for col in range(0, 4):
                r.M[row][col] = m.M[row][col]
        return r

    def add(self, m):
        for row in range(0, 4):
            for col in range(0, 4):
                self.M[row][col] = self.M[row][col] + m.M[row][col]

    def multiply(self, m):
        r = Matrix.identity()
        for row in range(0, 4):
            for col in range(0, 4):
                sum = 0
                for index in range(0, 4):
                    sum += self.M[row][index] * m.M[index][col]
                r.M[row][col] = sum
        self.M = r.M
        return self

    def translate(self, x, y, z):
        self.M = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [x, y, z, 1]]
        return self

    def scale(self, x, y, z):
        self.M = [[x, 0, 0, 0], [0, y, 0, 0], [0, 0, z, 0], [0, 0, 0, 1]]
        return self

    def rotate(self, ax, ay, az):
        ROTSEQX = 1 << 1
        ROTSEQY = 1 << 2
        ROTSEQZ = 1 << 3

        mrot = Matrix.identity()

        mx = Matrix.identity()
        my = Matrix.identity()
        mz = Matrix.identity()
        mtmp = Matrix.identity()
        sinTheta = 0
        cosTheta = 0
        rotSeq = 0

        if ax > 0:
            rotSeq = rotSeq | ROTSEQX

        if ay > 0:
            rotSeq = rotSeq | ROTSEQY

        if az > 0:
            rotSeq = rotSeq | ROTSEQZ

        if rotSeq == 0:
            self.M = mrot.M
            return self

        if rotSeq & ROTSEQX:
            cosTheta = Cos(ax)
            sinTheta = Sin(ax)

            mx.M = [
                [1, 0, 0, 0],
                [0, cosTheta, sinTheta, 0],
                [0, -sinTheta, cosTheta, 0],
                [0, 0, 0, 1],
            ]

            if rotSeq == ROTSEQX:
                mrot = Matrix.copy(mx)
                self.M = mrot.M
                return self

        if rotSeq & ROTSEQY:
            cosTheta = Cos(ay)
            sinTheta = Sin(ay)

            my.M = [
                [cosTheta, 0, -sinTheta, 0],
                [0, 1, 0, 0],
                [sinTheta, 0, cosTheta, 0],
                [0, 0, 0, 1],
            ]

            if rotSeq == ROTSEQX:
                mrot = Matrix.copy(my)
                self.M = mrot.M
                return self

        if rotSeq & ROTSEQZ:
            cosTheta = Cos(az)
            sinTheta = Sin(az)

            mz.M = [
                [cosTheta, sinTheta, 0, 0],
                [-sinTheta, cosTheta, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]

            if rotSeq == ROTSEQZ:
                mrot = Matrix.copy(mz)
                self.M = mrot.M
                return self

        if rotSeq & ROTSEQX:
            if rotSeq & ROTSEQY:
                if rotSeq & ROTSEQZ:
                    mtmp = Matrix.copy(mx).multiply(my)
                    mrot = Matrix.copy(mtmp).multiply(mz)
                    self.M = mrot.M
                    return self
                mrot = Matrix.copy(mx).multiply(my)
                self.M = mrot.M
                return self

        if rotSeq & ROTSEQZ:
            if rotSeq & ROTSEQX:
                mrot = Matrix.copy(mx).multiply(my)
                self.M = mrot.M
                return self
            mrot = Matrix.copy(my).multiply(mz)
            self.M = mrot.M
            return self

        self.M = mrot.M
        return self


class Vector:
    M = [0, 0, 0]

    def __init__(self, x=0, y=0, z=0):
        self.M = [x, y, z]

    @staticmethod
    def identity():
        v = Vector()
        v.M = [0, 0, 0]
        return v

    @staticmethod
    def right():
        v = Vector()
        v.M = [1, 0, 0]
        return v

    @staticmethod
    def copy(m):
        v = Vector.identity()
        for i in range(0, 3):
            v.M[i] = m.M[i]
        return v

    @property
    def x(self):
        return self.M[0]

    @property
    def y(self):
        return self.M[1]

    @property
    def z(self):
        return self.M[2]

    @x.setter
    def x(self, x):
        self.M[0] = x * 1

    @y.setter
    def y(self, y):
        self.M[1] = y * 1

    @z.setter
    def z(self, z):
        self.M[2] = z * 1

    def transform(self, m: Matrix):
        r = Vector.identity()
        for col in range(0, 3):
            sum = 0
            for row in range(0, 3):
                sum += self.M[row] * m.M[row][col]
            sum += m.M[3][col]
            r.M[col] = sum
        return r

    def add(self, v):
        self.x += v.x
        self.y += v.y
        self.z += v.z
        return self

    def subtract(self, v):
        self.x -= v.x
        self.y -= v.y
        self.z -= v.z
        return self

    def scale(self, s):
        self.x *= s
        self.y *= s
        self.z *= s
        return self

    def normalize(self):
        l = self.length()
        if (l) == 0:
            self.x = 0
            self.y = 0
            self.z = 0
            return self

        self.x = self.x / l
        self.y = self.y / l
        self.z = self.z / l
        return self

    def dot(self, vb):
        return (vb.x * self.x) + (vb.y * self.y) + (vb.z * self.z)

    def cross(self, vb):
        vr = Vector.identity()
        vr.x = (self.y * vb.z) - (self.z * vb.y)
        vr.y = (self.z * vb.x) - (self.x * vb.z)
        vr.z = (self.x * vb.y) - (self.y * vb.x)
        return vr

    def length(self):
        fx = self.x
        fy = self.y
        fz = self.z
        return Sqr(fx * fx + fy * fy + fz * fz)

    def angleTo(self, v):
        return angleTo(self.x, self.y, v.x, v.y)

    def distanceTo(self, v):
        vc = Vector.copy(v)
        vc.subtract(self)
        return vc.length()

    def __str__(self):
        return "({},{})".format(self.x, self.y)
