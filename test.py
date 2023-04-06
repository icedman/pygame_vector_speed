from maths import *
from track import *
import yaml

f = TrackFeature()
with open("./data/angle_1.yaml", mode="rt", encoding="utf-8") as file:
    yml = yaml.safe_load(file)
    f.loadDefinition(yml)

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

for t in f.segments:
    t.compute()

for t in f.segments:
    t.computeTrackPoints()

for t in f.segments:
    for p in t.points:
        print(p)


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
