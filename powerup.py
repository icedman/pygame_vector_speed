from entity import *
from data.objects import *
from state import *
from sounds import *


class PowerUp(Entity):
    active = True
    trackObject = None
    angle = 0

    def init(self):
        _ = self
        _.polygon = 0
        _.radius = 0.2
        _.shape = objects["objects"]["item_pickup"]
        _.active = False
        _.visible = False
        _.angle = 0

    def create(self):
        return PowerUp()

    def update(self, dt):
        _ = self
        if "rotate" in _.shape:
            _.angle += _.shape["rotate"] * dt / 1000
            _.direction = Vector.fromAngle(_.angle)
        Entity.update(self, dt)

        player = gameState.player
        for et in entityService.entities:
            for e in entityService.entities[et]:
                if e.trackPoint != None:
                    # activate power for enemies only if player is visible ;)
                    if player != None and e != player and e.distanceTo(player) > 10:
                        continue
                    d = e.trackPoint.index - _.trackObject.trackPoint.index
                    dd = Sqr(d * d)
                    _.visible = dd < 50
                    if _.visible and not _.active:
                        dist = _.pos.distanceTo(e.pos)
                        if dist < _.radius + e.radius:
                            _.activate(e)

    def activate(self, target):
        _ = self
        entityService.destroy(self)
        # todo random power ups
        entityService.createFloatingText(_.pos.x, _.pos.y, "+shield")
        target.shield += 100
        soundService.play(Effects.powerup)
        if target.shield > target.max_shield:
            target.max_shield = target.shield


class Arrow(PowerUp):
    def init(self):
        PowerUp.init(self)
        _ = self
        _.shape = objects["objects"]["track_arrow"]

    def create(self):
        return Arrow()

    def activate(self, target):
        _ = self


class SpeedPad(PowerUp):
    def init(self):
        PowerUp.init(self)
        _ = self
        _.shape = objects["objects"]["_speed_pad"]

    def create(self):
        return SpeedPad()

    def activate(self, target):
        _ = self
        _.active = True
        _.shape = objects["objects"]["_speed_pad_activated"]
        target.boost()
        soundService.play(Effects.speedpad)


class Mines(PowerUp):
    def init(self):
        PowerUp.init(self)
        _ = self
        _.shape = objects["objects"]["mines"]

    def create(self):
        return Mines()

    def activate(self, target):
        _ = self
        self.destroy()
        entityService.createParticles(_.pos.x, _.pos.y, 3, 1)
        entityService.attach(
            entityService.create(EntityType.explosion, _.pos.x, _.pos.y)
        )
        entityService.createFloatingText(_.pos.x, _.pos.y, "mines!!!").color = "white"
        target.damage(75)
        target.speed *= 0.5
        soundService.play(Effects.mines)

    # def update(self, dt):
    #     PowerUp.update(self, dt)
    #     _ = self
    #     if _.visible:
    #         _.mark("mines", Vector(0.8, -0.8), 3500)


class Shot(Entity):
    def init(self):
        PowerUp.init(self)
        _ = self
        _.shape = objects["objects"]["mines"]

    def create(self):
        return Shot()


entityService.defs[EntityType.powerUp] = PowerUp()
entityService.defs[EntityType.arrow] = Arrow()
entityService.defs[EntityType.speedPad] = SpeedPad()
entityService.defs[EntityType.mines] = Mines()
