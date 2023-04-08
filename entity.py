from maths import *


class Entity:
    pos = Vector.identity()
    direction = Vector.identity()
    speed = 0
    radius = 0.5
    _angle = 0

    # collision hint
    segment = None
    pointIndex = 0

    def __init__(self):
        self.angle = 0

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, a):
        self._angle = a
        self.direction = Vector.fromAngle(self.angle)

    def update(self, dt):
        _ = self
        _.pos.add(Vector.copy(_.direction).scale(_.speed))

    def throttleUp(self):
        _ = self
        _.speed += 0.005
        if _.speed > 0.3:
            _.speed = 0.3

    def throttleDown(self):
        _ = self
        _.speed += 0.01
        if _.speed < 0.1:
            _.speed = 0.1
