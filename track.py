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
    _rotateLeft = Matrix.identity().rotate(0, 90, 180 * 3.14 / 180)
    _rotateRight = Matrix.identity().rotate(0, 270, 180 * 3.14 / 180)

    position = Vector.identity()

    precision = 0.5

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

    points = []

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

    # move to mathss
    # def calculateAngle(self, f, t):
    #     right = Vector.right()
    #     angle = f.angleTo(t)
    #     return 360 - angle if (right.angleTo(to)) > 90 else angle

    def compute(self):
        _ = self
        if _.prevSegment:
            _.baseAngle = _.prevSegment.endAngle
            _.position = _.prevSegment.endPoint

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

        if _.nextSegment != None:
            _.nextSegment.baseAngle = _.endAngle

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

    def computeTrackPoints(self):
        _ = self
        _.trackPoints = []

        tw = _.trackWidth
        sw = _.splitWidth
        tw2 = tw / 2

        for i in range(0, len(_.points)):
            p = _.points[i]
            np = None
            if i < len(_.points)-1:
                np = _.points[i+1]
            elif _.nextSegment != None:
                np = _.nextSegment.points[0]
            else:
                break
            d = Vector.copy(np).subtract(p)
            d.normalize()

            sideDir = Vector(0,0,1).cross(d)
            sideDir.normalize()
            trackWidth = Vector.copy(sideDir).scale(tw2)
            railWidth = Vector.copy(sideDir).scale(tw2 * 0.5)
            borderWidth = Vector.copy(sideDir).scale(tw2 * 0.1)

            t = TrackPoint()
            t.outerTrack = Vector.copy(p).add(trackWidth)
            t.outerRail = Vector.copy(t.outerTrack).add(railWidth)
            t.outerBorder = Vector.copy(t.outerRail).add(borderWidth)
            t.innerTrack = Vector.copy(p).subtract(trackWidth)
            t.innerRail = Vector.copy(t.innerTrack).subtract(railWidth)
            t.innerBorder = Vector.copy(t.innerRail).subtract(borderWidth)
            t.point = Vector.copy(p)
            _.trackPoints.append(t)
        return


class TrackFeature:
    segments: []
    name = ""
    startAngle = 0

    def __init__(self):
        self.segments = []

    def loadDefinition(self, yml):
        _ = self
        _.name = yml["track"]
        _.startAngle = yml["startAngle"]

        _.segments = []
        prev = None
        for s in yml["segments"]:
            t = TrackSegment()
            t.loadDefinition(s)
            t.prevSegment = prev
            if prev != None:
                prev.nextSegment = t
            prev = t
            _.segments.append(t)



# class RaceTrack:
#     segments: []
#     points: []

