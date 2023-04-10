from maths import *
from draw import Context
from entity import *
from data.ships import *
from data.objects import *
from track import *

debug = {"entityVectors": False, "steerAssist": False, "collisionPoints": False}


def renderSegment(ctx, segment, dark=False):
    ctx.saveAttributes()
    ctx.state.strokeWidth = 1
    if dark:
        ctx.state.forcedColor = "Grey23"

    points = []
    outerTrack = []
    innerTrack = []
    outerRail = []
    innerRail = []
    outerBorder = []
    innerBorder = []

    t = segment
    segment.dark = dark
    for j in range(0, 2):
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

            if j == 1:
                break

        # attach track objects
        for obj in t.objects:
            if obj.rendered == False:
                obj.rendered = True
                p = entityService.create(
                    EntityType(EntityType.powerUp.value + obj.type.value),
                    obj.pos.x,
                    obj.pos.y,
                )
                p.trackObject = obj
                obj.entity = p
                p.direction = Vector.copy(obj.trackPoint.direction)
                entityService.attach(p)
                # print(obj.trackPoint.index)

        t = t.nextSegment
        if t == None:
            break

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

    # ctx.drawPolygonPoints(points, "grey42", False)
    ctx.drawPolygonPoints(outerTrack, "grey42", False)
    ctx.drawPolygonPoints(innerTrack, "grey42", False)
    ctx.drawPolygonPoints(outerRail, segment.color, False)
    ctx.drawPolygonPoints(innerRail, segment.color, False)
    ctx.drawPolygonPoints(outerBorder, segment.color, False)
    ctx.drawPolygonPoints(innerBorder, segment.color, False)

    ctx.restore()


def renderTrack(ctx, segment, entity):
    t = segment

    entitySegmentIndex = 0
    if entity.segment != None:
        entitySegmentIndex = entity.segment.index

    bucket = []

    while t != None:
        dark = False
        dx = entitySegmentIndex - t.index
        dist = Sqr(dx * dx)

        # segments behind of entity
        if dist > 2 and entitySegmentIndex > t.index:
            dark = True
        if dist > 4 and entitySegmentIndex > t.index:
            t = t.nextSegment
            continue
        # segments ahead of entity
        if dist > 4 and entitySegmentIndex < t.index:
            dark = True
        if dist > 8 and entitySegmentIndex < t.index:
            break

        # renderSegment(ctx, t, dark)
        bucket.insert(0, {"track": t, "dark": dark})
        t = t.nextSegment

    for item in bucket:
        renderSegment(ctx, item["track"], item["dark"])


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
    if not entity.visible:
        return

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
            entity.shape["shapes"],
            entity.pos.x,
            entity.pos.y,
            entity.radius,
            -90 + entity.direction.angle(),
            "cyan",
        )


def renderParticle(ctx, entity):
    v = Vector.copy(entity.pos).add(
        Vector.copy(entity.direction).scale(-entity.radius * entity.speed)
    )
    ctx.drawLine(entity.pos.x, entity.pos.y, v.x, v.y, RndOr("red", "orange"))


def renderFloatingText(ctx, entity):
    ctx.drawText(entity.pos.x, entity.pos.y, entity.text, entity.radius, entity.color)


def renderMines(ctx, entity):
    renderDefault(ctx, entity)


def renderShip(ctx, entity):
    ctx.saveAttributes()

    if entity.trackPoint != None and entity.trackPoint.segment.dark:
        ctx.state.forcedColor = "Grey23"

    # trail
    trailOffset = Vector.copy(entity.direction).scale(-0.15)
    ctx.state.strokeWidth = 2
    points = []
    sz = 0.001
    for i in range(0, len(entity.trail) - 1):
        v = Vector.copy(entity.trail[i])
        v.add(trailOffset)
        points.append([v.x + Rand(-1, 1) * sz, v.y + Rand(-1, 1) * sz])
    if len(points) > 2:
        ctx.drawPolygonPoints(points, RndOr("yellow", "white"), False)
    ctx.state.strokeWidth = 1
    points = []
    for i in range(0, len(entity.trail) - 2):
        v = Vector.copy(entity.trail[i])
        v.add(trailOffset)
        points.append([v.x + Rand(-1, 1) * sz, v.y + Rand(-1, 1) * sz])
    if len(points) > 2:
        ctx.drawPolygonPoints(points, RndOr("red", "orange"), False)

    ctx.state.strokeWidth = 2
    renderDefault(ctx, entity)

    if debug["steerAssist"]:
        if entity.trackPoint != None and entity.targetPoint != None:
            p1 = Vector.copy(entity.trackPoint.point)
            p2 = Vector.copy(entity.targetPoint.point)
            ctx.drawPolygon(p2.x, p2.y, 0.25, 12, "cyan")
            ctx.drawLine(p1.x, p1.y, p2.x, p2.y, "cyan")

    ctx.restore()


class Renderer:
    defs: dict[EntityType, any] = {
        EntityType.ship: renderShip,
        EntityType.enemyShip: renderShip,
        EntityType.particle: renderParticle,
        EntityType.explosion: renderDefault,
        EntityType.floatingText: renderFloatingText,
        EntityType.powerUp: renderDefault,
        EntityType.arrow: renderDefault,
        EntityType.speedPad: renderDefault,
        EntityType.mines: renderMines,
    }

    @staticmethod
    def renderEntity(ctx: Context, e: Entity):
        r = Renderer.defs[e.type]
        r(ctx, e)
        renderDebug(ctx, e)
