from maths import *

class Entity:
    pos = Vector.identity()
    direction = Vector.identity()
    speed = 1
    radius = 0.5

    # collision hint
    segment = None
    pointIndex = 0
