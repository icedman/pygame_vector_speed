from entity import *


class Particle(Entity):
    def init(self):
        _ = self
        _.polygon = 0
        _.radius = 1
        _.ttl = 1250

    def create(self):
        return Particle()

    def update(self, dt):
        _ = self
        Entity.update(self, dt)


class FloatingText(Particle):
    text = ""

    def init(self):
        _ = self
        _.radius = 0.02
        _.ttl = 2500

    def create(self):
        return FloatingText()


def createParticles(x, y, count):
    for i in range(0, count):
        v = Vector.fromAngle(Rand(0, 360)).normalize().scale(0.01 + 0.01 * Rnd())
        xx = x + v.x
        yy = y + v.y
        d = Vector(xx, yy).subtract(Vector(x, y)).normalize()
        p = entityService.create(EntityType.particle, xx, yy)
        p.direction = d
        p.speed = 0.05
        entityService.attach(p)


def createFloatingText(x, y, text):
    p = entityService.create(EntityType.floatingText, x, y)
    p.text = text
    p.direction = Vector(1, 1)
    p.speed = 0.01
    entityService.attach(p)
