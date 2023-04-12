from scene import *
from maths import *
from draw import Context
from renderer import *
from scene import *
from state import *
from game import *
from generator import *
from track import *


class Frame(Scene):
    ticks = 0
    frameTicks = 0
    text = ""
    start = None
    length = 2000
    opts = None

    def __init__(self, length, text="", start=None, opts=None):
        _ = self
        _.ticks = 0
        _.frameTicks = 0
        _.length = length
        if text != None:
            _.text = text
        if start != None:
            _.start = start

    def onEnter(self):
        pass

    def onUpdate(self, dt):
        if self.ticks == 0:
            self.onEnter()
        self.ticks += dt

    def onRender(self, gfx):
        size = [gameState.screenWidth, gameState.screenHeight]
        tt = self.text.split("\n")
        y = 0
        for t in tt:
            gfx.drawText(size[0] / 2, size[1] - 40 + y, t, 2)
            y += 24


class FrameLines(Frame):
    segments = None

    def onEnter(self):
        track = TrackGenerator()
        track.addSector([TrackSegment.randomArcSegment()])
        self.segments = track.segments

    def onRender(self, gfx):
        Frame.onRender(self, gfx)
        if self.segments == None:
            return
        size = [gameState.screenWidth, gameState.screenHeight]

        # camera
        segments = self.segments
        midSegment = Floor(len(segments) / 2)
        targetSegment = segments[midSegment]
        mid = Floor(len(targetSegment.trackPoints) / 2)
        targetPoint = targetSegment.trackPoints[mid].point

        scale = 50
        gfx.scale(scale, scale)
        cam = gfx.transform(targetPoint)
        if gameState.cam != None:
            cam.scale(4).add(gameState.cam).scale(1 / 5)
        gameState.cam = Vector.copy(cam)
        gfx.translate(size[0] / 2 - cam.x, size[1] / 2 - cam.y)

        # renderTrack(gfx, track.segments[0], gameState.player)
        for segment in segments:
            segment.color = [255, 0, 0]
            renderSegment(
                gfx,
                segment,
                False,
                {
                    "objects": False,
                    "line": False,
                    "section_track": True,
                    "section_rail": False,
                    "border": True,
                    "rail": True,
                    "track": True,
                },
            )


class DemoScene(Scene):
    ticks = 0
    track = TrackGenerator()
    frames = []

    def onEnter(self):
        _ = self
        _.ticks = 0
        _.frames = []
        _.frames.append(FrameLines(2000, "123", None))
        _.frames.append(Frame(2000, "456"))
        _.frames.append(FrameLines(2000, "789"))
        pass

    def onExit(self):
        pass

    def getFrames(self, ticks):
        res = []
        totalLength = 0
        for f in self.frames:
            if f.start != None:
                if ticks >= f.start and ticks < f.start + f.length:
                    f.frameTicks = f.ticks + f.start
                    res.append(f)
                continue
            s = totalLength
            if ticks >= s and ticks < s + f.length:
                f.frameTicks = f.ticks + s
                res.append(f)
            totalLength += f.length
        return res

    def onUpdate(self, dt):
        _ = self
        if gameState.released["escape"]:
            # sceneService.enterScene(SceneType.menu)
            gameState.done = True
            return

        frames = _.getFrames(_.ticks)
        for f in frames:
            f.onUpdate(dt)

        _.ticks += dt

    def onRender(self, gfx):
        _ = self
        track = _.track

        gfx.save()
        gfx.clear("black")

        frames = _.getFrames(_.ticks)
        for f in frames:
            f.onRender(gfx)

        gfx.restore()
