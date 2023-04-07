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
    carDir = Vector.identity()


class TrackSegment:
    position = Vector.identity()

    precision = 0.5

    points = []
    trackPoints = []
    railType = 0
    trackColor = 0
    id = 0
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
        # _.points = []
        # _.position = Vector.identity()
        # _.endPoint = Vector.identity()
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

        if _.length >= 4 and (Rand(0, 1000) % 100) < 30:
            _.splitWidth = 0.15 + Rnd(0, 0.35)

        # split disabled
        if _.sector < 4:
            _.splitWidth = 0

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

    def computeTrackPoints(self):
        _ = self
        _.trackPoints = []

        tw = _.trackWidth
        mtw = tw if tw < 1 else 1
        rw = mtw * 0.5
        bw = mtw * 0.1
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
            t.outerTrack = Vector.copy(p).add(trackWidth)
            t.outerRail = Vector.copy(t.outerTrack).add(railWidth)
            t.outerBorder = Vector.copy(t.outerRail).add(borderWidth)
            t.innerTrack = Vector.copy(p).subtract(trackWidth)
            t.innerRail = Vector.copy(t.innerTrack).subtract(railWidth)
            t.innerBorder = Vector.copy(t.innerRail).subtract(borderWidth)
            t.point = Vector.copy(p)
            _.trackPoints.append(t)


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
        lastIdx = 0
        if count > 0:
            lastIdx = count - 1
            lastSegment = self.segments[lastIdx]
            sector = lastSegment.sector + 1

        prev = lastSegment
        for ss in segments:
            s = TrackSegment.copy(ss)
            s.sector = sector
            if prev != None:
                prev.nextSegment = s
                s.prevSegment = prev

                # smoothen width transition
                w = 1
                s.trackWidth += prev.trackWidth * w
                s.trackWidth /= w + 1

            prev = s
            self.segments.append(s)

        lastIdx -= 1
        if lastIdx < 0:
            lastIdx = 0

        self.compute(lastIdx)

    def compute(self, startIdx=0):
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
            s.computeTrackPoints()
