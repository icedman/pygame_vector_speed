from maths import *
from track import *
from generator import *
import yaml

with open("./data/sources/ships.yaml", mode="rt", encoding="utf-8") as file:
    yml = yaml.safe_load(file)
    print(yml)

g = TrackGenerator()
g.randomFeature("angle")
g.randomSector(2)
