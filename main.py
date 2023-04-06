import pygame
from maths import *
from draw import Context
from track import *

import yaml

track = Track()
for i in range(0, 100):
    track.addSector(
        [
            TrackSegment.randomArcSegment(),
            TrackSegment.randomLineSegment(),
            TrackSegment.randomArcSegment(),
        ]
    )

# f = TrackFeature()
# with open("./data/angle_1.yaml", mode="rt", encoding="utf-8") as file:
#     yml = yaml.safe_load(file)
#     f.loadDefinition(yml)


# def generate_track():
#     f.segments = [
#         TrackSegment.randomArcSegment(),
#         TrackSegment.randomLineSegment(),
#         TrackSegment.randomArcSegment(),
#     ]

#     prev = None
#     for t in f.segments:
#         if prev != None:
#             prev.nextSegment = t
#             t.prevSegment = prev
#         prev = t

#     for t in f.segments:
#         t.compute()

#     for t in f.segments:
#         t.computeTrackPoints()


# generate_track()

pygame.init()
# size = [1600, 900]
size = [1280, 800]
screen = pygame.display.set_mode(size)
done = False
gfx = Context(screen)

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
        idx -= 2
    if pressed[pygame.K_DOWN]:
        idx += 2
    # if released[pygame.K_LEFT]:
    #     generate_track()
    
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

            if dist > 2:
                continue

            tp = None if i >= len(t.trackPoints) - 1 else t.trackPoints[i]
            if tp != None:
                outerTrack.append([tp.outerTrack.x, tp.outerTrack.y])
                outerRail.append([tp.outerRail.x, tp.outerRail.y])
                outerBorder.append([tp.outerBorder.x, tp.outerBorder.y])
                innerTrack.append([tp.innerTrack.x, tp.innerTrack.y])
                innerRail.append([tp.innerRail.x, tp.innerRail.y])
                innerBorder.append([tp.innerBorder.x, tp.innerBorder.y])

    scale = 50
    gfx.scale(scale, scale)
    # gfx.rotate(rot)

    idx = (idx + len(points)) % len(points)
    l = points[idx]
    v = gfx.transform(Vector(l[0], l[1]))
    gfx.translate(size[0] / 2 - v.x, size[1] / 2 - v.y)

    # gfx.drawPolygonPoints(points, "red", False)
    gfx.drawPolygonPoints(outerTrack, "white", False)
    gfx.drawPolygonPoints(innerTrack, "yellow", False)
    gfx.drawPolygonPoints(outerRail, "white", False)
    gfx.drawPolygonPoints(innerRail, "yellow", False)
    gfx.drawPolygonPoints(outerBorder, "magenta", False)
    gfx.drawPolygonPoints(innerBorder, "magenta", False)
    gfx.restore()

    pygame.display.flip()

    rot += 1
