from maths import *
from draw import Context
from entity import *
from data.ships import *
from data.objects import *
from track import *

debug = {"entityVectors": False, "steerAssist": False, "collisionPoints": False}


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

                # debug collision points
                if debug["collisionPoints"]:
                    for c in tp.outerCollisionPoints:
                        # ctx.drawPolygon(c.x, c.y, 0.25, 12, "red")
                        x = Vector.copy(c).add(Vector.copy(tp.sideDir).scale(-0.25))
                        ctx.drawLine(x.x, x.y, c.x, c.y, "green")
                    for c in tp.innerCollisionPoints:
                        # ctx.drawPolygon(c.x, c.y, 0.25, 12, "red")
                        x = Vector.copy(c).add(Vector.copy(tp.sideDir).scale(0.25))
                        ctx.drawLine(x.x, x.y, c.x, c.y, "green")

        t = t.nextSegment

    for i in range(0, len(outerTrack) - 1):
        p1 = outerTrack[i]
        p2 = innerTrack[i]
        v1 = Vector(p1[0], p1[1])
        v2 = Vector(p2[0], p2[1])
        ctx.drawLine(p1[0], p1[1], p2[0], p2[1], "grey42")

    for i in range(0, len(outerTrack) - 1):
        p1 = outerTrack[i]
        p2 = outerRail[i + 1]
        ctx.drawLine(p1[0], p1[1], p2[0], p2[1], "grey42")
        p1 = innerTrack[i]
        p2 = innerRail[i + 1]
        ctx.drawLine(p1[0], p1[1], p2[0], p2[1], "grey42")

    ctx.drawPolygonPoints(points, "grey42", False)
    ctx.drawPolygonPoints(outerTrack, "white", False)
    ctx.drawPolygonPoints(outerRail, "white", False)
    ctx.drawPolygonPoints(innerTrack, "yellow", False)
    ctx.drawPolygonPoints(innerRail, "yellow", False)


def renderDebug(ctx, entity):
    if debug["entityVectors"]:
        ctx.drawPolygon(entity.pos.x, entity.pos.y, entity.radius, 12, "red")
        d = Vector.copy(entity.pos).add(
            Vector.copy(entity.direction).scale(entity.radius)
        )
        ctx.drawLine(entity.pos.x, entity.pos.y, d.x, d.y, "cyan")
        d = Vector.copy(entity.pos).add(
            Vector.copy(entity.velocity).normalize().scale(entity.radius * 2)
        )
        ctx.drawLine(entity.pos.x, entity.pos.y, d.x, d.y, "cyan")


def renderDefault(ctx, entity):
    if entity.polygon > 0:
        ctx.drawPolygon(
            entity.pos.x,
            entity.pos.y,
            entity.radius,
            entity.polygon,
            "red",
        )

    if entity.shape != None:
        ctx.drawShape(
            entity.shape,
            entity.pos.x,
            entity.pos.y,
            entity.radius,
            -90 + entity.direction.angle(),
            "red",
        )


def renderParticle(ctx, entity):
    v = Vector.copy(entity.pos).add(
        Vector.copy(entity.direction).scale(-entity.radius * entity.speed)
    )
    ctx.drawLine(entity.pos.x, entity.pos.y, v.x, v.y, "red")


def renderFloatingText(ctx, entity):
    ctx.drawText(entity.pos.x, entity.pos.y, entity.text, entity.radius, "red")


def renderShip(ctx, entity):
    renderDefault(ctx, entity)

    if debug["steerAssist"]:
        if entity.trackPoint != None and entity.targetPoint != None:
            p1 = Vector.copy(entity.trackPoint.point)
            p2 = Vector.copy(entity.targetPoint.point)
            ctx.drawPolygon(p2.x, p2.y, 0.25, 12, "cyan")
            ctx.drawLine(p1.x, p1.y, p2.x, p2.y, "cyan")


class Renderer:
    defs: dict[EntityType, any] = {
        EntityType.ship: renderShip,
        EntityType.particle: renderParticle,
        EntityType.floatingText: renderFloatingText,
    }

    @staticmethod
    def renderEntity(ctx: Context, e: Entity):
        r = Renderer.defs[e.type]
        r(ctx, e)
        renderDebug(ctx, e)
