from entity import *
from track import *
from maths import *
from state import *


class Ship(Entity):
    track = None
    steer = 0
    throttle = 0
    trail = []
    ai = False
    travel = 0
    meter = 0

    boost_t = 0
    damage_t = 0
    collide_t = 0

    # parameters
    max_speed = 0.8
    max_shield = 10000
    shield = 1000
    indestructible = False

    race_position = 0

    def init(self):
        _ = self
        _.shape = ships["objects"]["ship_3"]
        _.steer = 0
        _.throttle = 0
        _.trail = []
        _.radius = 0.3
        _.ai = False
        _.travel = 0
        _.meter = 0

        _.direction = Vector.identity()

        _.boost_t = 0
        _.collide_t = 0
        _.max_speed = 0.8
        _.max_shield = 10000
        _.shield = _.max_shield
        _.indestructible = False

    def create(self):
        return Ship()

    def boost(self):
        _ = self
        if _.boost_t <= 0:
            _.boost_t = 1250

    def damage(self, amount=50):
        _ = self
        if _.indestructible:
            return
        _.shield -= amount
        _.damage_t = 500

        if _.shield <= 0:
            self.disable()

    def disable(self):
        _ = self
        _.shield = 0
        _.speed = 0
        _.boost_t = 0
        _.damage_t = 0
        _.collide_t = 0
        _.trail = []
        self.visible = False
        entityService.createParticles(_.pos.x, _.pos.y, 3, 1)
        entityService.attach(
            entityService.create(EntityType.explosion, _.pos.x, _.pos.y)
        )
        gameState.gameOver = True

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

        if _.shield <= 0:
            return

        # input
        if _.throttle > 0:
            _.throttle -= 100 * dt / 1000
            if _.throttle < 0:
                _.throttle = 0
            _.speed += 0.0025
        elif _.throttle < 0:
            _.throttle += 100 * dt / 1000
            if _.throttle > 0:
                _.throttle = 0
            _.speed -= 0.002

        if _.steer != 0:
            angle = _.direction.angle()
            if _.steer > 0:
                _.steer -= 100 * dt / 1000
                if _.steer < 0:
                    _.steer = 0
                angle += 80 * dt / 1000
            elif _.steer < 0:
                _.steer += 100 * dt / 1000
                if _.steer > 0:
                    _.steer = 0
                angle -= 80 * dt / 1000
            vd = Vector.fromAngle(angle).normalize()
            _.direction = vd

        # cap
        if _.speed > _.max_speed:
            _.speed = _.max_speed
        if _.speed < -0.1:
            _.speed = -0.1

        s = _.speed
        boostSpeed = 0
        if _.boost_t > 0:
            _.boost_t -= dt
            if _.collide_t <= 0:
                boostSpeed = 0.2

        vn = Vector.copy(_.velocity).normalize()

        # collide other ships
        _.race_position = 1
        others = self.otherShips()
        for o in others:
            if o.trackPoint.index > _.trackPoint.index:
                _.race_position += 1
            m = self.distanceTo(o)
            if m != None and m < 4:
                dist = o.pos.distanceTo(_.pos)
                if dist < o.radius + _.radius:
                    repel = Vector.copy(o.pos).subtract(_.pos).normalize()

                    cp = Vector.copy(_.pos).add(Vector.copy(repel).scale(dist * 0.5))
                    parts = entityService.createParticles(cp.x, cp.y, Rand(1, 2))
                    for pp in parts:
                        pp.ttl = 250
                        pp.speed = 0.05

                    o.pos.add(Vector.copy(repel).scale(dist * 0.2))
                    _.pos.add(Vector.copy(repel).scale(dist * -0.2))
                    o.damage(10)
                    _.damage(10)

        # apply force
        if _.track != None:
            # collision detection
            cc = None
            pre = 4
            for i in range(0, pre):
                v = Vector.copy(vn).scale(((s + boostSpeed) * 20) / 1000 * dt / pre)
                _.pos.add(v)
                col = _.track.detectCollision(self)
                if col != None:
                    _.collide_t = 200
                    _.pos.add(col["vector"])
                    cc = col
            if cc != None:
                _.damage()
                cf = cc["force"]
                _.speed *= 1 - cf
                if _.speed < 0.01:
                    _.speed = 0.01
                s = _.speed
                _.velocity.add(Vector.copy(cc["vector"]).scale(2 * cf))
                vn = Vector.copy(_.velocity).normalize()
                if s > 0.02 and cf > 0.08:
                    cp = cc["collisionPoint"]
                    entityService.createParticles(
                        cp.x, cp.y, 1 + Floor(Rand(0, 4) * cf)
                    )
        else:
            v = Vector.copy(vn).scale(((s + boostSpeed) * 20) / 1000 * dt)
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

        if _.ai:
            _.autoDrive()

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

        if _.damage_t > 0:
            _.damage_t -= dt

        # meter
        meter = Floor(s * 1000)
        if _.meter < meter:
            _.meter += 1
        elif _.meter > meter:
            _.meter -= 1

        # travel
        if _.trackPoint != None:
            travel = (_.trackPoint.index - 5) * 4.5
            if _.travel < travel:
                _.travel += 1

    def autoDrive(self):
        _ = self
        if _.trackPoint != None:
            s = _.speed
            target = None
            if s > 0.07:
                tp = TrackPoint.advance(_.trackPoint, 4)
                target = Vector.copy(tp.point)
            else:
                tp = TrackPoint.advance(_.trackPoint, 2)
                target = Vector.copy(tp.point)
            steerTo = Vector.copy(target).subtract(_.pos).normalize()
            targetAngle = steerTo.angle()
            fromAngle = _.direction.angle()
            angleSteerLeft = fromAngle + 10
            angleSteerRight = fromAngle - 10
            dl = targetAngle - angleSteerLeft
            dr = targetAngle - angleSteerRight
            distL = Sqr(dl * dl)
            distR = Sqr(dr * dr)
            if distL > distR:
                _.steerLeft()
                dist = distL
            else:
                _.steerRight()
                dist = distR
            if dist > 20:
                _.throttleDown()
            elif _.ai:
                _.throttleUp()
            # ai cheats
            if _.collide_t > 0:
                _.direction = Vector.copy(steerTo).normalize()
            #     _.pos.add(Vector.copy(_.direction).scale(0.001))

    def distanceTo(self, entity):
        _ = self
        if _.trackPoint == None or entity.trackPoint == None:
            return None
        dx = entity.trackPoint.index - _.trackPoint.index
        return Sqr(dx * dx)

    def otherShips(self):
        res = []
        for et in entityService.entities:
            for e in entityService.entities[et]:
                if not isinstance(e, Ship):
                    break
                if e == self:
                    continue
                res.append(e)
        return res

    def setGraphics(self, name):
        self.shape = ships["objects"][name]


class EnemyShip(Ship):
    def init(self):
        Ship.init(self)
        _ = self
        _.shape = ships["objects"]["ship_2"]
        _.max_speed = 0.6
        _.ai = True
        _.indestructible = True
        # _.boost()

    def create(self):
        return EnemyShip()

    def update(self, dt):
        _ = self

        # reposition if needed
        player = gameState.player
        if player == None:
            return

        dist = _.distanceTo(player)
        if dist == None:
            return

        # slow down way ahead
        if dist > 60 and _.trackPoint.index > player.trackPoint.index:
            _.speed = 0

        # slow down if nearing last segment
        if dist > 10 and _.segment == _.track.segments[len(_.track.segments) - 1]:
            _.speed = 0

        # catch up when pruned
        if _.segment == None or _.segment.pruned == True:
            _.segment = _.track.segments[0]
            _.trackPoint = _.segment.trackPoints[Floor(len(_.segment.trackPoints) / 2)]

        # catch up
        if dist > 60 and _.trackPoint.index < player.trackPoint.index:
            _.trackPoint = TrackPoint.advance(_.trackPoint, 20)

        Ship.update(self, dt)


entityService.defs[EntityType.ship] = Ship()
entityService.defs[EntityType.enemyShip] = EnemyShip()
