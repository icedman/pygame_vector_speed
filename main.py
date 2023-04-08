import pygame
from maths import *
from draw import Context
from track import *
from generator import *
from renderer import *
from entity import *
from particles import *
from ship import *

entityService.defs[EntityType.ship] = Ship()
entityService.defs[EntityType.particle] = Particle()
entityService.defs[EntityType.floatingText] = FloatingText()
entityService.createParticles = createParticles
entityService.createFloatingText = createFloatingText

track = TrackGenerator()
track.buildStart()

pygame.init()
# size = [1600, 900]
size = [1280, 800]
screen = pygame.display.set_mode(size)
done = False
gfx = Context(screen)
gfx.state.strokeWidth = 1


def cull(v1, v2):
    w = size[0]
    h = size[1]
    if (v1.x < 0 and v2.x < 0) or (v1.y < 0 and v2.y < 0):
        return True
    if (v1.x > w and v2.x > w) or (v1.y > h and v2.y > h):
        return True
    return False


gfx.cull = cull

trackKeys = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
keys = {}
released = {}

rot = 0
off = 0
obj = entityService.attach(entityService.create(EntityType.ship))
obj.radius = 0.3
track.addToStartingGrid(obj)

# entityService.createFloatingText(obj.pos.x, obj.pos.y, "+20")

last_tick = 0
while not done:
    tick = pygame.time.get_ticks()
    dt = tick - last_tick
    if dt < 16:
        continue
    last_tick = tick

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_ESCAPE]:
        done = True

    for k in trackKeys:
        released[k] = k in keys and keys[k] == True and pressed[k] == False
        keys[k] = pressed[k]

    if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
        obj.steerLeft()
    if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
        obj.steerRight()
    if pressed[pygame.K_UP] or pressed[pygame.K_w]:
        obj.throttleUp()
    if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
        obj.throttleDown()
    # else:
    #     obj.throttleUp()

    entityService.update(dt)
    if obj.segment != None:
        track.buildSector(obj.segment.sector, 2, 2)
        track.prune(obj.segment.sector, 4)

    gfx.clear("black")
    gfx.save()
    gfx.drawRect(0, 0, size[0], size[1], "red")

    scale = 90 - (40 * obj.speed / 1)
    gfx.scale(scale, scale)

    # camera
    cam = gfx.transform(
        Vector.copy(obj.pos).add(
            Vector.copy(obj.direction).scale(obj.radius * 3 + (obj.radius * obj.speed))
        )
    )
    gfx.translate(size[0] / 2 - cam.x, size[1] / 2 - cam.y)

    gfx.saveAttributes()
    gfx.state.strokeWidth = 1
    gfx.state.forcedColor = "Grey30"
    renderTrack(gfx, track.segments[0], obj.segment, 8)
    # renderTrack(gfx, track.segments[0], TrackSegment.advance(obj.segment, 5), 2)
    gfx.restore()
    renderTrack(gfx, track.segments[0], obj.segment, 3)

    rad = obj.radius
    col = track.detectCollision(obj)
    if col != None:
        obj.pos.add(col["vector"])
        obj.speed *= 1 - col["force"]
        if obj.speed < 0.01:
            obj.speed = 0.01
        gfx.saveAttributes()
        gfx.strokeWidth = 4
        gfx.drawRect(2, 2, size[0] - 4, size[1] - 4, "magenta")
        gfx.restore()
        cp = col["collisionPoint"]
        # gfx.drawPolygon(cp.x, cp.y, 0.5, 8, "yellow")
        if col["force"] > 0.08:
            entityService.createParticles(
                cp.x, cp.y, 1 + Floor(Rand(0, 2) * col["force"])
            )
    # else:
    #     obj.throttleUp()

    for t in entityService.entities:
        for e in entityService.entities[t]:
            Renderer.renderEntity(gfx, e)

    gfx.restore()

    pygame.display.flip()

    rot += 1
