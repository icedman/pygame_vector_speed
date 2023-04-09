from entity import *
from track import *


class Ship(Entity):
    track = None
    steer = 0
    throttle = 0
    trail = []

    collide_t = 0

    def init(self):
        _ = self
        _.shape = ships["objects"]["ship_3"]
        _.steer = 0
        _.throttle = 0
        _.trail = []

    def create(self):
        return Ship()

    def throttleUp(self):
        _ = self
        _.throttle = 1

    def throttleDown(self):
        _ = self
        _.throttle = -1
        if _.speed > 0.2 and Rand(0, 100) < 15:
            entityService.createParticles(_.pos.x, _.pos.y, 1 + Floor(Rand(0, 2)))

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

        # apply force
        if _.track != None:
            # collision detection
            pre = 2
            for i in range(0, pre):
                v = Vector.copy(vn).scale((s * 20) / 1000 * dt / pre)
                _.pos.add(v)
                col = _.track.detectCollision(self)
                if col != None:
                    _.collide_t = 200
                    _.pos.add(col["vector"])
                    cf = col["force"]
                    _.speed *= 1 - cf
                    if _.speed < 0.01:
                        _.speed = 0.01
                    s = _.speed
                    _.velocity.add(Vector.copy(col["vector"]).scale(2 * cf))
                    vn = Vector.copy(_.velocity).normalize()
                    if s > 0.02 and cf > 0.08:
                        cp = col["collisionPoint"]
                        entityService.createParticles(
                            cp.x, cp.y, 1 + Floor(Rand(0, 4) * cf)
                        )
        else:
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

        # save trail
        _.trail.append(Vector.copy(_.pos))
        while len(_.trail) > 6:
            del _.trail[0]

        # random particles
        if _.collide_t > 0:
            _.collide_t -= dt
        else:
            if s > 0.01 and Rand(0, 100) < 5:
                entityService.createParticles(_.pos.x, _.pos.y, 1 + Floor(Rand(0, 2)))
            _.throttleUp()


entityService.defs[EntityType.ship] = Ship()
