from maths import *
from track import *
from generator import *
import yaml

from data.angle_1 import *
from data.angle_2 import *
from data.chicane_1 import *
from data.chicane_2 import *
from data.hairpin import *
from data.loop_1 import *
from data.loop_2 import *

with open("./data/sources/ships.yaml", mode="rt", encoding="utf-8") as file:
    yml = yaml.safe_load(file)
    print(yml)

g = TrackGenerator()
sources = [
    angle_1,
    angle_2,
    chicane_1,
    chicane_2,
    hairpin,
    loop_1,
    loop_2,
]

f = None
for src in sources:
    f = g.loadFeature(src)

#     yml = yaml.safe_load(file)
#     f.loadDefinition(yml)

#     segments = []
#     prev = None
#     for s in yml["segments"]:
#         t = TrackSegment()
#         t.loadDefinition(s)
#         if prev != None:
#             prev.nextSegment = t
#         prev = t
#         segments.append(t)

#     for t in segments:
#         t.compute()

# for t in segments:
#     for p in t.points:
#         print(p)

# for t in f.segments:
#     t.compute()

# for t in f.segments:
#     t.computeTrackPoints()

# for t in f.segments:
#     for p in t.points:
#         print(p)


# t = TrackSegment()
# t.baseAngle = 45
# t.length = 10
# t.compute()
# for p in t.points:
#     print(p)

# t = TrackSegment()
# t.segmentType = TrackSegmentType.ARC_RIGHT
# t.arc = 20
# t.startRadius = 10
# t.endRadius = 20
# t.compute()
# for p in t.points:
#     print(p)
