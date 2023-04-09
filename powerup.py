from entity import *
from data.objects import *
from state import *


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
        if player != None and player.trackPoint != None:
            d = player.trackPoint.index - _.trackObject.trackPoint.index
            dd = Sqr(d * d)
            _.visible = dd < 25
            if _.visible:
                dist = _.pos.distanceTo(player.pos)
                if dist < _.radius + player.radius:
                    _.activate()

    def activate(self):
        _ = self
        entityService.destroy(self)
        entityService.createFloatingText(_.pos.x, _.pos.y, "+20")


class Arrow(PowerUp):
    def init(self):
        PowerUp.init(self)
        _ = self
        _.shape = objects["objects"]["track_arrow"]

    def create(self):
        return Arrow()

    def activate(self):
        _ = self


class SpeedPad(PowerUp):
    def init(self):
        PowerUp.init(self)
        _ = self
        _.shape = objects["objects"]["_speed_pad"]

    def create(self):
        return SpeedPad()

    def activate(self):
        _ = self


class Mines(PowerUp):
    def init(self):
        PowerUp.init(self)
        _ = self
        _.shape = objects["objects"]["mines"]

    def create(self):
        return Mines()

    def activate(self):
        _ = self
        entityService.destroy(self)
        entityService.createParticles(_.pos.x, _.pos.y, 3, 1)
        entityService.attach(
            entityService.create(EntityType.explosion, _.pos.x, _.pos.y)
        )


entityService.defs[EntityType.powerUp] = PowerUp()
entityService.defs[EntityType.arrow] = Arrow()
entityService.defs[EntityType.speedPad] = SpeedPad()
entityService.defs[EntityType.mines] = Mines()
