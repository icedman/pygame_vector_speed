import pygame
from maths import *
from draw import Context
from track import *
from generator import *
from entity import *
from data.angle_1 import *
from data.angle_2 import *
from data.loop_1 import *
from data.loop_2 import *
from renderer import *

feature = TrackFeature()
feature.loadDefinition(loop_2)

ship = ships["objects"][2]["shapes"]

track = TrackGenerator()
track.buildStart()

for i in range(0, 3):
    # track.addSector(feature.copySegments())
    track.addSector(feature.copySegments())
    # track.compute()
    track.addSector(
        [
            TrackSegment.randomArcSegment(),
            TrackSegment.randomLineSegment(),
            TrackSegment.randomArcSegment(),
        ]
    )
    track.addSector(feature.copySegments())

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
obj = Entity()
obj.radius = 0.3
obj.pos = Vector.copy(track.segments[1].trackPoints[0].point)

last_tick = 0
while not done:
    tick = pygame.time.get_ticks()
    dt = tick - last_tick
    if dt < 24:
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

    if pressed[pygame.K_LEFT]:
        obj.angle -= 2
    if pressed[pygame.K_RIGHT]:
        obj.angle += 2
    if pressed[pygame.K_UP]:
        obj.throttleUp()
    if pressed[pygame.K_DOWN]:
        obj.throttleDown()
    # else:
    #     obj.throttleUp()

    obj.update(dt)

    gfx.clear("black")
    gfx.save()
    gfx.drawRect(0, 0, size[0], size[1], "red")

    scale = 90
    gfx.scale(scale, scale)

    v = gfx.transform(Vector.copy(obj.pos))
    gfx.translate(size[0] / 2 - v.x, size[1] / 2 - v.y)

    gfx.saveAttributes()
    gfx.state.strokeWidth = 1
    gfx.state.forcedColor = "grey"
    renderTrack(gfx, track.segments[0], TrackSegment.advance(obj.segment, 2), 6)
    gfx.restore()
    renderTrack(gfx, track.segments[0], obj.segment, 2)

    rad = obj.radius
    col = track.detectCollision(obj)
    if col != None:
        obj.pos.add(col["vector"])
        obj.speed *= 1 - col["force"]
        if obj.speed < 0:
            obj.speed = 0

    renderEntity(gfx, obj)

    gfx.restore()

    pygame.display.flip()

    rot += 1
