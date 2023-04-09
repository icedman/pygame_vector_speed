from enum import Enum
from maths import *


class TrackSegmentType(Enum):
    STRAIGHT = 0
    ARC_LEFT = 1
    ARC_RIGHT = 2
    START = 3
    FINISH = 4


class TrackPoint:
    index = 0
    point = Vector.identity()
    outerTrack = Vector.identity()
    innerTrack = Vector.identity()
    outerRail = Vector.identity()
    innerRail = Vector.identity()
    outerSplit = Vector.identity()
    innerSplit = Vector.identity()
    outerBorder = Vector.identity()
    innerBorder = Vector.identity()
    sideDir = Vector.identity()
    direction = Vector.identity()

    outerCollisionPoints = []
    innerCollisionPoints = []

    segment = None
    nextPoint = None

    @staticmethod
    def advance(t, count):
        if t == None:
            return None
        for i in range(0, count):
            if t.nextPoint == None:
                break
            t = t.nextPoint
        return t


# powerUp = 40
# arrow = 41
# speedPad = 42
# mines = 43


class TrackObjectType(Enum):
    POWERUP = 0
    ARROW = 1
    SPEEDPAD = 2
    MINES = 3


class TrackObject:
    type = TrackObjectType.POWERUP
    pos = Vector.identity()
    rendered = False
    segment = None
    trackPoint = None
    entity = None

    def __init__(self, segment, trackPoint):
        _ = self
        _.segment = segment
        _.trackPoint = trackPoint
        _.rendered = False
        _.entity = None


class TrackSegment:
    position = Vector.identity()

    precision = 0.5

    points = []
    trackPoints = []
    railType = 0
    trackColor = 0
    index = 0
    sector = 0

    segmentType = TrackSegmentType.STRAIGHT
    arc = 2
    length = 4
    startRadius = 1
    endRadius = 1
    outerRail = 0.5
    innerRail = 0.5
    trackWidth = 2
    splitWidth = 0

    # computed
    objects = 0
    baseAngle = 0
    startAngle = 0
    endAngle = 0
    endPoint = Vector.identity()

    prevSegment = None
    nextSegment = None

    objects = []

    # render hit
    color = "white"
    dark = False
    pruned = False

    def __init__(self):
        _ = self
        _.points = []
        _.trackPoints = []
        _.objects = []

    @staticmethod
    def copy(t):
        _ = TrackSegment()
        _.segmentType = t.segmentType
        _.arc = t.arc
        _.length = t.length
        _.startRadius = t.startRadius
        _.endRadius = t.endRadius
        _.outerRail = t.outerRail
        _.innerRail = t.innerRail
        _.trackWidth = t.trackWidth
        _.splitWidth = t.splitWidth
        return t

    def loadDefinition(self, yml):
        _ = self
        _.segmentType = TrackSegmentType(yml["segment"])
        _.arc = yml["arc"]
        _.length = yml["length"]
        _.startRadius = yml["startRadius"]
        _.endRadius = yml["endRadius"]
        _.outerRail = yml["outerRail"]
        _.innerRail = yml["innerRail"]
        _.trackWidth = yml["trackWidth"]
        _.splitWidth = yml["splitWidth"]

    @staticmethod
    def randomLineSegment():
        _ = TrackSegment()
        _.segmentType = TrackSegmentType.STRAIGHT
        width = 0.5 + Rnd(0, 2)
        innerRail = 0.35 + Rnd(0, 0.5)
        outerRail = 0.35 + Rnd(0, 0.5)

        if (Rand(0, 100) % 4) != 0:
            innerRail = outerRail

        _.trackWidth = width
        _.innerRail = innerRail
        _.outerRail = outerRail
        _.length = 2 + Rnd(0, 16)

        # if _.length >= 4 and (Rand(0, 1000) % 100) < 30:
        #     _.splitWidth = 0.15 + Rnd(0, 0.35)

        return _

    @staticmethod
    def randomArcSegment():
        _ = TrackSegment.randomLineSegment()
        arc = 25 + Rnd(0, (360 - 25 - 60))
        if arc > 100:
            arc = arc / 2

        radius = 0.05 + Rnd(0, 0.5)
        _.arc = Floor(arc)
        _.startRadius = radius
        _.endRadius = radius
        _.segmentType = TrackSegmentType.ARC_LEFT
        if RndOr(0, 1) == 0:
            _.segmentType = TrackSegmentType.ARC_RIGHT

        if _.arc > 120:
            _.arc -= Floor(Rnd(0, 80))

        if _.arc > 100:
            _.arc = Floor(_.arc / 2)

        return _

    @staticmethod
    def advance(t, count):
        if t == None:
            return None
        for i in range(0, count):
            if t.nextSegment == None:
                break
            t = t.nextSegment
        return t

    def compute(self):
        _ = self
        _.points = []
        if _.prevSegment:
            _.baseAngle = _.prevSegment.endAngle
            _.position = Vector.copy(_.prevSegment.endPoint)

        if (
            _.segmentType == TrackSegmentType.STRAIGHT
            or _.segmentType == TrackSegmentType.START
        ):
            if _.segmentType == TrackSegmentType.START:
                _.splitWidth = 0
            _.computeStraight()

        if (
            _.segmentType == TrackSegmentType.ARC_LEFT
            or _.segmentType == TrackSegmentType.ARC_RIGHT
        ):
            _.computeArc()

        if _.segmentType == TrackSegmentType.FINISH:
            _.splitWidth = 0
            _.computeEnd()

    def computeStraight(self, length=None):
        _ = self
        if length != None:
            _.length = length
        _.arc = 0
        _.startRadius = 0
        _.endRadius = 0

        _.points = []

        start = Vector.copy(_.position)
        _.endPoint = Vector.copy(start)
        _.points.append(Vector.copy(start))

        pre = _.precision

        division = (int)(_.length / pre)
        for i in range(0, division):
            angle = _.baseAngle
            heading = Vector.identity()
            heading.x = Cos(angle * 0.0174533)
            heading.y = Sin(angle * 0.0174533)
            heading.normalize()
            heading.scale(pre)

            end = Vector.copy(start).add(heading)
            _.points.append(end)
            _.endPoint = end
            _.endAngle = angle

            start = Vector.copy(end)

    def computeArc(self, arc=None):
        _ = self
        if arc != None:
            _.arc = arc
        _.length = 0

        _.points = []

        start = Vector.copy(_.position)
        _.endPoint = start
        _.points.append(Vector.copy(start))

        angle = _.baseAngle
        rad = _.startRadius
        radIncrement = (_.endRadius - _.startRadius) / _.arc
        dir = 1 if _.segmentType == TrackSegmentType.ARC_LEFT else -1
        for i in range(0, _.arc):
            angle = angle + dir
            heading = Vector.identity()
            heading.x = Cos(angle * 0.0174533)
            heading.y = Sin(angle * 0.0174533)
            heading.normalize()
            heading.scale(rad)
            rad += radIncrement

            point = Vector.copy(start).add(heading)
            _.points.append(point)
            _.endPoint = point
            _.endAngle = angle

            start = Vector.copy(point)

    def computeEnd(self, nextSegment=None):
        _ = self
        if nextSegment != None:
            _.nextSegment = nextSegment
        _.arc = 0
        _.startRadius = 0
        _.endRadius = 0
        _.length = 0

        _.points = []

        start = Vector.copy(_.position)
        _.endPoint = Vector.copy(start)
        _.points.append(Vector.copy(start))

        end = Vector.copy(_.nextSegment.position)
        angle = baseAngle
        current = start
        target = end

        pre = _.precision

        moveAngle = 4.0
        rad = pre * 0.25
        prevDistance = 0
        for i in range(0, 400):
            heading = Vector.identity()
            angle1 = angle + moveAngle
            heading.x = Cos(angle1 * 0.0174533)
            heading.y = Sin(angle1 * 0.0174533)
            heading.normalize()
            heading.scale(rad)
            newPos1 = Vector.copy(current).add(heading)

            angle2 = angle - moveAngle
            heading = Vector.identity()
            heading.x = Cos(angle2 * 0.0174533)
            heading.y = Sin(angle2 * 0.0174533)
            heading.normalize()
            heading.scale(rad)
            newPos2 = Vector.copy(current).add(heading)

            d1 = Vector3.Distance(target, newPos1)
            d2 = Vector3.Distance(target, newPos2)
            if d1 < d2:
                current = Vector.copy(newPos1)
                angle = angle1
                prevDistance = d1
            else:
                current = Vector.copy(newPos2)
                angle = angle2
                prevDistance = d2

            _.points.append(Vector.copy(current))

            if prevDistance < 0.5:
                break

        _.points.append(Vector.copy(end))

    @staticmethod
    def _smoothenVectors(points, pre, count=1):
        for c in range(0, count):
            for i in range(0, len(points) - 2):
                p1 = points[i]
                p2 = points[i + 1]
                p3 = points[i + 2]
                v1 = Vector.copy(p2).subtract(p1)
                v1.normalize().scale(pre).add(p1)
                v2 = Vector.copy(p2).subtract(p3)
                v2.normalize().scale(pre).add(p3)
                v3 = v1.add(v2).scale(0.5)
                points[i + 1] = v3

    def computeTrackPoints(self, index=0):
        _ = self
        _.trackPoints = []

        tw = _.trackWidth
        mtw = tw if tw < 1 else 1
        rw = mtw * 0.7
        bw = mtw * 0.35
        sw = _.splitWidth
        tw2 = tw / 2
        rw2 = rw / 2
        bw2 = bw / 2

        pre = _.precision + 0.2

        # precision correction
        pp = []
        prev = None
        for i in range(0, len(_.points)):
            p = _.points[i]
            if prev != None:
                dist = p.distanceTo(prev)
                if dist < pre:
                    continue
            prev = p
            pp.append(p)

        _.points = pp

        # smoothen distances
        TrackSegment._smoothenVectors(_.points, pre, 4)

        for i in range(0, len(_.points)):
            p = Vector.copy(_.points[i])
            np = None
            if i < len(_.points) - 1:
                np = Vector.copy(_.points[i + 1])
            elif _.nextSegment != None:
                np = _.nextSegment.points[0]
            else:
                break
            d = Vector.copy(np).subtract(p)
            d.normalize()

            sideDir = Vector(0, 0, 1).cross(d)
            sideDir.normalize()
            trackWidth = Vector.copy(sideDir).scale(tw2)
            railWidth = Vector.copy(sideDir).scale(rw2)
            borderWidth = Vector.copy(sideDir).scale(bw2)

            t = TrackPoint()
            t.direction = Vector.copy(d)
            t.sideDir = Vector.copy(sideDir)
            t.outerTrack = Vector.copy(p).add(trackWidth)
            t.outerRail = Vector.copy(t.outerTrack).add(railWidth)
            t.outerBorder = Vector.copy(t.outerRail).add(borderWidth)
            t.innerTrack = Vector.copy(p).subtract(trackWidth)
            t.innerRail = Vector.copy(t.innerTrack).subtract(railWidth)
            t.innerBorder = Vector.copy(t.innerRail).subtract(borderWidth)
            t.point = Vector.copy(p)
            t.index = index
            t.segment = _
            index += 1
            _.trackPoints.append(t)

    def computeCollisionPoints(self):
        _ = self
        inc = 0.25
        for i in range(0, len(_.trackPoints)):
            p1 = _.trackPoints[i]
            p1.outerCollisionPoints = []
            p1.innerCollisionPoints = []
            p2 = None
            if i < len(_.trackPoints) - 2:
                p2 = _.trackPoints[i + 1]
            else:
                if _.nextSegment != None:
                    p2 = _.nextSegment.trackPoints[0]
            if p2 == None:
                break

            p1.nextPoint = p2

            for j in range(0, 2):
                v1 = p1.outerRail if j == 0 else p1.innerRail
                v2 = p2.outerRail if j == 0 else p2.innerRail
                vdir = Vector.copy(v2).subtract(v1).normalize().scale(inc)
                l = v1.distanceTo(v2)
                cnt = Floor(l / inc)
                for k in range(0, Floor(cnt) + 1):
                    v3 = Vector.copy(v1).add(Vector.copy(vdir).scale(k))
                    d = v3.distanceTo(p1.point)
                    if d < _.trackWidth / 2:
                        continue
                    if j == 0:
                        p1.outerCollisionPoints.append(v3)
                    else:
                        p1.innerCollisionPoints.append(v3)


class TrackFeature:
    segments: []
    name = ""
    startAngle = 0

    defs = None

    def __init__(self):
        self.segments = []

    def loadDefinition(self, yml):
        _ = self
        _.defs = yml
        _.name = yml["track"]
        _.startAngle = yml["startAngle"]
        _.segments = []
        for s in yml["segments"]:
            t = TrackSegment()
            t.loadDefinition(s)
            _.segments.append(t)

    def copySegments(self):
        self.loadDefinition(self.defs)
        return self.segments


class Track:
    segments = []

    def __init__(self):
        self.segments = []
        return

    def addSector(self, segments):
        sector = 0
        count = len(self.segments)
        lastSegment = None
        idx = 0
        if count > 0:
            idx = count - 1
            lastSegment = self.segments[idx]
            sector = lastSegment.sector + 1

        prev = lastSegment
        for ss in segments:
            s = TrackSegment.copy(ss)
            # s.trackWidth *= 1.25
            s.sector = sector
            if prev != None:
                prev.nextSegment = s
                s.prevSegment = prev
                s.index = prev.index + 1

                # smoothen width transition
                w = 1
                s.trackWidth += prev.trackWidth * w
                s.trackWidth /= w + 1

            prev = s
            self.segments.append(s)

        idx -= 1
        if idx < 0:
            idx = 0

        self.compute(idx)

    def compute(self, startIdx=0):
        index = 0
        seg = self.segments[startIdx]
        if seg.prevSegment != None:
            index = seg.trackPoints[len(seg.trackPoints) - 1].index + 1
        prev = None
        for i in range(startIdx, len(self.segments)):
            s = self.segments[i]
            if prev != None:
                prev.nextSegment = s
                s.prevSegment = prev
            prev = s

        for i in range(startIdx, len(self.segments)):
            s = self.segments[i]
            s.compute()

        for i in range(startIdx, len(self.segments)):
            s = self.segments[i]
            s.computeTrackPoints(index)
            index += len(s.trackPoints)

        for i in range(startIdx, len(self.segments)):
            s = self.segments[i]
            s.computeCollisionPoints()

    def detectCollision(self, entity):
        _ = self
        rad = entity.radius * 0.95
        bounce = 1
        isWithin = False
        startIdx = 0
        try:
            startIdx = _.segments.index(entity.segment) - 1
        except:
            startIdx = 0
        if startIdx < 0:
            startIdx = 0

        nearestDistance = -1

        pointIndex = 0
        segmentIndex = 0
        if entity.segment != None:
            segmentIndex = entity.segment.index
        entity.segment = None
        for idx in range(startIdx, len(_.segments)):
            seg = _.segments[idx]

            dx = segmentIndex - seg.index
            dist = Sqr(dx * dx)
            if dist > 4:
                continue

            for p in seg.trackPoints:
                # skip points check as much as possible
                pdist = p.point.distanceTo(entity.pos)
                if pdist > seg.trackWidth * 3:
                    if isWithin:
                        return None
                    continue

                if not isWithin:
                    entity.segment = seg
                isWithin = True
                pointIndex += 1

                if isWithin and pdist < nearestDistance or nearestDistance == -1:
                    entity.trackPoint = p
                    nearestDistance = pdist

                if pointIndex > 10:
                    return None

                for k in range(0, 2):
                    barrier = (
                        p.outerCollisionPoints if k == 0 else p.innerCollisionPoints
                    )
                    for c in barrier:
                        dirSign = -1 if k == 0 else 1
                        if c.distanceTo(entity.pos) < rad:
                            cross = Vector.copy(c).add(
                                Vector.copy(p.sideDir).scale(rad * dirSign)
                            )
                            dist = cross.distanceTo(entity.pos)
                            vector = Vector.copy(p.sideDir).scale(
                                dist * bounce * dirSign
                            )
                            if dist == 0:
                                return None
                            return {
                                "segment": seg,
                                "force": dist,
                                "trackPoint": p,
                                "collisionPoint": c,
                                "vector": vector,
                            }

        return None

    def attachToTrackPoint(self, entity, tp):
        entity.track = self
        entity.segment = tp.segment
        entity.trackPoint = tp
        entity.targetPoint = TrackPoint.advance(tp, 4)
        entity.pos = Vector.copy(tp.point)
        entity.direction = Vector.copy(tp.direction)

    def attachToStartingGrid(self, entity, offset=0):
        _ = self
        segment = _.segments[0]
        tp = segment.trackPoints[Floor(len(segment.trackPoints) / 3) + offset]
        self.attachToTrackPoint(entity, tp)
