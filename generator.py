from maths import *
from track import *


class TrackGenerator(Track):
    defs = {}

    def __init__(self):
        Track.__init__(self)
        return

    def loadDefinition(self, yml):
        # print(yml)
        return

    def loadFeature(self, yml):
        f = TrackFeature()
        f.loadDefinition(yml)
        featureType = f.name.split("_")[0]
        if not featureType in self.defs:
            self.defs[featureType] = []
        self.defs[featureType].append(f)
        return f

    def buildStart(self):
        self.segments = []
        seg = TrackSegment.randomLineSegment()
        seg.baseAngle = -65
        seg.trackWidth = 1.5
        self.addSector([seg])

    def buildSector(self, sector, distance):
        return

    def prune(self, sector):
        return
