from entity import *
from track import *


class Ship(Entity):
    steer = 0
    throttle = 0

    def init(self):
        _ = self
        _.shape = ships["objects"]["ship_3"]["shapes"]
        _.steer = 0
        _.throttle = 0

    def create(self):
        return Ship()

    def throttleUp(self):
        _ = self
        _.throttle = 1

    def throttleDown(self):
        _ = self
        _.throttle = -1

    def steerLeft(self):
        _ = self
        _.steer = -1

    def steerRight(self):
        _ = self
        _.steer = 1

    def update(self, dt):
        _ = self

        # input
        if _.throttle > 0:
            _.throttle -= 0.5 * dt
            if _.throttle < 0:
                _.throttle = 0
            _.speed += 0.0025
        elif _.throttle < 0:
            _.throttle += 0.5 * dt
            if _.throttle > 0:
                _.throttle = 0
            _.speed -= 0.002

        angle = _.direction.angle()
        if _.steer > 0:
            _.steer -= 0.5 * dt
            if _.steer < 0:
                _.steer = 0
            angle += 80 * dt / 1000
        elif _.steer < 0:
            _.steer += 0.5 * dt
            if _.steer > 0:
                _.steer = 0
            angle -= 80 * dt / 1000
        _.direction = Vector.fromAngle(angle).normalize()

        # cap
        if _.speed > 0.8:
            _.speed = 0.8
        if _.speed < -0.1:
            _.speed = -0.1

        s = _.speed
        vn = Vector.copy(_.velocity).normalize()

        # push
        v = Vector.copy(vn).scale((s * 20) / 1000 * dt)
        _.pos.add(v)

        # steer
        _.velocity = (
            Vector.copy(vn).scale(8).add(_.direction).scale(1 / 9).normalize().scale(s)
        )

        # steer assist
        if _.trackPoint != None and s > 0.07:
            tp = TrackPoint.advance(_.trackPoint, 4)
            if tp != _.trackPoint:
                _.targetPoint = tp
            if _.targetPoint != None:
                trackDir = (
                    Vector.copy(_.targetPoint.point)
                    .subtract(_.trackPoint.point)
                    .normalize()
                )
                vn = Vector.copy(_.direction)
                _.direction = (
                    Vector.copy(vn).scale(8).add(trackDir).scale(1 / 9).normalize()
                )
