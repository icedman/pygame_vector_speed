import pygame
from maths import *
from draw import Context
from track import *

from data.angle_1 import *
from data.ships import *

feature = TrackFeature()
feature.loadDefinition(angle_1)

ship = ships["objects"][2]["shapes"]

track = Track()


for i in range(0, 4):
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

current_sector = 0
rot = 0
last_tick = 0
idx = 0
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

    if pressed[pygame.K_UP]:
        idx -= 1
    if pressed[pygame.K_DOWN]:
        idx += 1

    gfx.clear("black")
    gfx.save()
    gfx.drawRect(0, 0, size[0], size[1], "red")

    points = []
    outerTrack = []
    innerTrack = []
    outerRail = []
    innerRail = []
    outerBorder = []
    innerBorder = []
    for t in track.segments:
        for i in range(0, len(t.points)):
            p = t.points[i]
            points.append([p.x, p.y])

            if len(points) - 1 == idx:
                current_sector = t.sector

            dx = t.sector - current_sector
            dist = Sqr(dx * dx)
            if dist > 1:
                continue

            tp = None if i >= len(t.trackPoints) - 1 else t.trackPoints[i]
            if tp != None:
                outerTrack.append([tp.outerTrack.x, tp.outerTrack.y])
                outerRail.append([tp.outerRail.x, tp.outerRail.y])
                outerBorder.append([tp.outerBorder.x, tp.outerBorder.y])
                innerTrack.append([tp.innerTrack.x, tp.innerTrack.y])
                innerRail.append([tp.innerRail.x, tp.innerRail.y])
                innerBorder.append([tp.innerBorder.x, tp.innerBorder.y])

    scale = 40
    gfx.scale(scale, scale)

    idx = (idx + len(points)) % len(points)
    l = points[idx]
    v = gfx.transform(Vector(l[0], l[1]))
    gfx.translate(size[0] / 2 - v.x, size[1] / 2 - v.y)

    for i in range(0, len(outerTrack) - 1):
        p1 = outerTrack[i]
        p2 = innerTrack[i]
        # gfx.drawLine(p1[0], p1[1], p2[0], p2[1], "red")

    for i in range(0, len(outerTrack) - 1):
        p1 = outerTrack[i]
        p2 = outerRail[i + 1]
        # gfx.drawLine(p1[0], p1[1], p2[0], p2[1], "red")
        p1 = innerTrack[i]
        p2 = innerRail[i + 1]
        # gfx.drawLine(p1[0], p1[1], p2[0], p2[1], "red")

    gfx.drawPolygonPoints(points, "red", False)
    gfx.drawPolygonPoints(outerTrack, "white", False)
    gfx.drawPolygonPoints(innerTrack, "yellow", False)
    gfx.drawPolygonPoints(outerRail, "white", False)
    gfx.drawPolygonPoints(innerRail, "yellow", False)
    gfx.drawPolygonPoints(outerBorder, "magenta", False)
    gfx.drawPolygonPoints(innerBorder, "magenta", False)

    gfx.drawShape(ship, l[0], l[1], 0.2, 0, "red")

    gfx.restore()

    pygame.display.flip()

    rot += 1
