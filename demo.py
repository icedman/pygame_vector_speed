from scene import *
from maths import *
from draw import Context
from renderer import *
from scene import *
from state import *
from game import *
from generator import *
from track import *


class DemoScene(Scene):
    track = TrackGenerator()

    def onEnter(self):
        pass

    def onExit(self):
        pass

    def onUpdate(self, dt):
        _ = self
        if gameState.released["escape"]:
            # sceneService.enterScene(SceneType.menu)
            gameState.done = True
            return

    def onRender(self, gfx):
        _ = self
        size = [gameState.screenWidth, gameState.screenHeight]
        track = _.track

        gfx.save()
        gfx.clear("black")

        random.seed(0)

        track.segments = []

        # feature = track.defs["hairpin"][1]
        # track.addSector(feature.copySegments())

        # track.addSector([TrackSegment.randomLineSegment()])
        track.addSector([TrackSegment.randomArcSegment()])

        # camera
        midSegment = Floor(len(track.segments)/2)
        targetSegment = track.segments[midSegment]
        mid = Floor(len(targetSegment.trackPoints)/2)
        targetPoint = targetSegment.trackPoints[mid].point

        scale = 20
        gfx.scale(scale, scale)
        cam = gfx.transform(targetPoint)
        if gameState.cam != None:
            cam.scale(4).add(gameState.cam).scale(1 / 5)
        gameState.cam = Vector.copy(cam)
        gfx.translate(size[0] / 2 - cam.x, size[1] / 2 - cam.y)

        # renderTrack(gfx, track.segments[0], gameState.player)
        for segment in track.segments:
            renderSegment(gfx, segment, False, False)

        gfx.restore()
