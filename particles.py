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
        Entity.update(self, dt)


class FloatingText(Particle):
    text = ""

    def init(self):
        _ = self
        _.radius = 0.02
        _.ttl = 2500

    def create(self):
        return FloatingText()


class Explosion(Particle):
    def init(self):
        Particle.init(self)
        _ = self
        _.radius = 0.05
        _.polygon = 12
        _.ttl = 450

    def create(self):
        return Explosion()

    def update(self, dt):
        self.radius += 0.05
        self.radius *= 1.2
        Entity.update(self, dt)


def _createParticles(x, y, count, speed=0.05):
    for i in range(0, count):
        v = Vector.fromAngle(Rand(0, 360)).normalize().scale(0.01 + 0.01 * Rnd())
        xx = x + v.x
        yy = y + v.y
        d = Vector(xx, yy).subtract(Vector(x, y)).normalize()
        p = entityService.create(EntityType.particle, xx, yy)
        p.direction = d
        p.speed = 0.05
        entityService.attach(p)


def createExplosion(x, y, count):
    for i in range(0, count):
        _createParticles(
            x + Rand(-2, 2) * 0.05, y + Rand(-2, 2) * 0.05, Rand(2, 8), 0.25
        )


def createParticles(x, y, count, type=0):
    if type == 0:
        _createParticles(x, y, count)
    elif type == 1:
        createExplosion(x, y, count)


def createFloatingText(x, y, text):
    p = entityService.create(EntityType.floatingText, x, y)
    p.text = text
    p.direction = Vector(1, 1)
    p.speed = 0.01
    entityService.attach(p)


entityService.defs[EntityType.particle] = Particle()
entityService.defs[EntityType.explosion] = Explosion()
entityService.defs[EntityType.floatingText] = FloatingText()
entityService.createParticles = createParticles
entityService.createFloatingText = createFloatingText
