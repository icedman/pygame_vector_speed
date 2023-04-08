from maths import *
from draw import Context
from entity import *
from data.ships import *
from data.objects import *


def renderTrack(ctx, segment, startSegment=None, distance=8):
    points = []
    outerTrack = []
    innerTrack = []
    outerRail = []
    innerRail = []
    outerBorder = []
    innerBorder = []

    segmentIndex = 0
    if startSegment != None:
        segmentIndex = startSegment.index

    renderedDistance = 0

    t = segment
    while t != None:
        dx = segmentIndex - t.index
        dist = Sqr(dx * dx)
        if dist > distance:
            t = t.nextSegment
            continue
        for i in range(0, len(t.trackPoints)):
            tp = t.trackPoints[i]
            points.append([tp.point.x, tp.point.y])
            tp = None if i >= len(t.trackPoints) - 1 else t.trackPoints[i]
            if tp != None:
                outerTrack.append([tp.outerTrack.x, tp.outerTrack.y])
                outerRail.append([tp.outerRail.x, tp.outerRail.y])
                outerBorder.append([tp.outerBorder.x, tp.outerBorder.y])
                innerTrack.append([tp.innerTrack.x, tp.innerTrack.y])
                innerRail.append([tp.innerRail.x, tp.innerRail.y])
                innerBorder.append([tp.innerBorder.x, tp.innerBorder.y])
                renderedDistance += 1
        t = t.nextSegment

    for i in range(0, len(outerTrack) - 1):
        p1 = outerTrack[i]
        p2 = innerTrack[i]
        v1 = Vector(p1[0], p1[1])
        v2 = Vector(p2[0], p2[1])
        ctx.drawLine(p1[0], p1[1], p2[0], p2[1], "red")

    for i in range(0, len(outerTrack) - 1):
        p1 = outerTrack[i]
        p2 = outerRail[i + 1]
        ctx.drawLine(p1[0], p1[1], p2[0], p2[1], "red")
        p1 = innerTrack[i]
        p2 = innerRail[i + 1]
        ctx.drawLine(p1[0], p1[1], p2[0], p2[1], "red")

    ctx.drawPolygonPoints(points, "red", False)
    ctx.drawPolygonPoints(outerTrack, "white", False)
    ctx.drawPolygonPoints(innerTrack, "yellow", False)
    ctx.drawPolygonPoints(outerRail, "white", False)
    ctx.drawPolygonPoints(innerRail, "yellow", False)


def renderEntity(ctx, entity):
    ctx.drawPolygon(entity.pos.x, entity.pos.y, entity.radius, 12, "red")
    d = Vector.copy(entity.pos).add(Vector.copy(entity.direction).scale(entity.radius))
    ctx.drawLine(entity.pos.x, entity.pos.y, d.x, d.y, "cyan")

    ctx.drawShape(
        ships["objects"][2]["shapes"],
        entity.pos.x,
        entity.pos.y,
        entity.radius,
        entity.angle - 90,
        "red",
    )
    return
