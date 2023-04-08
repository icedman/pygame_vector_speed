import random

from maths import *
from track import *

from data.sectors import *
from data.angle_1 import *
from data.angle_2 import *
from data.chicane_1 import *
from data.chicane_2 import *
from data.hairpin import *
from data.loop_1 import *
from data.loop_2 import *


class TrackGenerator(Track):
    defs = {}

    def __init__(self):
        Track.__init__(self)

        sources = [
            angle_1,
            angle_2,
            chicane_1,
            chicane_2,
            hairpin,
            loop_1,
            loop_2,
        ]

        self.loadSectors(sectors)
        for src in sources:
            self.loadFeature(src)

    def loadSectors(self, yml):
        self.defs["sectors"] = yml["sectors"]

    def loadFeature(self, yml):
        f = TrackFeature()
        f.loadDefinition(yml)
        featureType = f.name.split("_")[0]
        if not featureType in self.defs:
            self.defs[featureType] = []
        self.defs[featureType].append(f)
        return f

    def buildStart(self):
        random.seed(777)

        self.segments = []
        seg = TrackSegment.randomLineSegment()
        seg.baseAngle = -65 + 360
        seg.trackWidth = 1.5
        seg.length = 4
        self.addSector([seg, TrackSegment.randomLineSegment()])
        self.addSector(self.randomSector(0))

    def buildSector(self, sector, distance, threshold):
        last = self.segments[len(self.segments) - 1]
        if (last.sector - sector) < threshold:
            for i in range(0, distance):
                self.addSector(self.randomSector(last.sector))

    def prune(self, sector, distance):
        first = self.segments[0]
        if sector - first.sector > distance:
            del self.segments[0]

    def randomFeature(self, type):
        features = self.defs[type]
        idx = Rand(0, 100) % len(features)
        return features[idx].copySegments()

    def randomSector(self, index):
        _ = self
        if not "sectors" in _.defs:
            return [TrackSegment.randomLineSegment()]

        sectors = _.defs["sectors"]
        index = index % len(sectors)
        sector = sectors[index]

        feature = ""
        score = 0

        for f in sector["features"]:
            if f == "randoms":
                continue
            ff = sector["features"][f]
            ss = ff * Rand(0, 100)
            if (ss > 0 and ss > score) or feature == "":
                score = ss
                feature = f

        if feature == "straights":
            return [TrackSegment.randomLineSegment()]
        elif feature == "angles":
            return self.randomFeature("angle")
        elif feature == "arcs":
            return [TrackSegment.randomArcSegment()]
        elif feature == "loops":
            return self.randomFeature("loop")
        elif feature == "chicanes":
            return self.randomFeature("chicane")
        elif feature == "hairpins":
            return self.randomFeature("hairpin")

        return [TrackSegment.randomLineSegment()]
