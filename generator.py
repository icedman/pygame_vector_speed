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
