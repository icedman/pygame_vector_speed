from maths import *
from track import *
from generator import *
import yaml

g = TrackGenerator()
with open("./data/sectors.yaml", mode="rt", encoding="utf-8") as file:
    yml = yaml.safe_load(file)
    g.loadDefinition(yml)

sources = [
    "./data/angle_1.yaml",
    "./data/angle_2.yaml",
    "./data/chicane_1.yaml",
    "./data/chicane_2.yaml",
    "./data/hairpin.yaml",
    "./data/loop_1.yaml",
    "./data/loop_2.yaml",
]

for src in sources:
    with open(src, mode="rt", encoding="utf-8") as file:
        yml = yaml.safe_load(file)
        g.loadFeature(yml)

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
