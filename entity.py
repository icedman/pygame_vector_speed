import enum
from maths import *
from track import *
from data.ships import *


class EntityType(Enum):
    ship = 1
    particle = 2
    floatingText = 3
    none = 100


class Entity:
    type: EntityType = EntityType.none
    shape = None
    polygon = 0
    radius = 0.5
    ttl = 0

    pos = Vector.identity()
    direction = Vector.identity()
    velocity = Vector.identity()

    # collision hint
    segment = None
    trackPoint = None
    targetPoint = None
    pointIndex = 0

    @property
    def speed(self):
        return self.velocity.length()

    @speed.setter
    def speed(self, a):
        _ = self
        if _.speed == 0:
            _.velocity = Vector.copy(_.direction)
        _.velocity.normalize().scale(a)

    # override these
    def init(self):
        return

    def create(self):
        return Entity()

    def control(self):
        return

    def update(self, dt):
        _ = self
        s = _.speed
        vn = Vector.copy(_.velocity).normalize()

        # push
        v = Vector.copy(vn).scale((s * 20) / 1000 * dt)
        _.pos.add(v)

        # steer
        _.velocity = (
            Vector.copy(vn).scale(8).add(_.direction).scale(1 / 9).normalize().scale(s)
        )


class EntityService:
    entities = {}
    enemies = {}

    createParticles: any
    createFloatingText: any

    defs = {
        EntityType.ship: None,
        EntityType.particle: None,
        EntityType.floatingText: None,
    }

    def __init__(self):
        self.init()

    def init(self):
        for k in self.defs.keys():
            self.entities[k] = []
            # if k in [
            #     EntityType.ship,
            # ]:
            #     self.enemies[k] = self.entities[k]

    def create(self, what, x=0, y=0):
        e = self.defs[what].create()
        e.init()
        e.pos = Vector(x, y)
        e.type = what
        return e

    def attach(self, e):
        base = self.defs[e.type]
        self.entities[e.type].append(e)
        return e

    def destroy(self, e: Entity):
        try:
            idx = self.entities[e.type].index(e)
            if idx != -1:
                del self.entities[e.type][idx]
        except:
            # could have been removed already (like a shot's life expiriing while also killing a enemy)
            return

    def update(self, dt):
        for t in self.entities:
            for e in self.entities[t]:
                e.update(dt)
                if e.ttl > 0:
                    e.ttl -= dt
                    if e.ttl <= 0:
                        self.destroy(e)


entityService = EntityService()
