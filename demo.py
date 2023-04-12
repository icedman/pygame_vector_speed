from scene import *
from maths import *
from draw import Context
from renderer import *
from scene import *
from state import *
from ship import *
from game import *
from generator import *
from track import *
from colors import *


class Frame(Scene):
    entered = False
    ticks = 0
    frameTicks = 0
    text = ""
    textOpts = {}
    start = None
    length = 2000
    opts = {}

    def __init__(self, length, text="", start=None, textOpts=None):
        _ = self
        _.ticks = 0
        _.frameTicks = 0
        _.length = length
        if text != None:
            _.text = text
        if start != None:
            _.start = start
        _.textOpts = {"size": 2, "color": "yellow", "align": "center"}
        if textOpts != None:
            for t in textOpts:
                _.textOpts[t] = textOpts[t]

        self.opts = {
            "scale": 90,
            "objects": False,
            "line": False,
            "section_track": False,
            "section_rail": False,
            "border": False,
            "rail": False,
            "track": False,
            "entityVectors": False,
            "steerAssist": False,
            "collisionPoints": False,
        }

    def onEnter(self):
        pass

    def onUpdate(self, dt):
        pass

    def onRender(self, gfx):
        size = [gameState.screenWidth, gameState.screenHeight]
        tt = self.text.split("\n")
        y = 0

        gfx.saveAttributes()
        if self.textOpts["size"] > 2:
            gfx.state.strokeWidth = 3
        for t in tt:
            yy = size[1] / 2 - 40 + y
            if self.textOpts["align"] == "bottom":
                yy = size[1] - 80 + y
            gfx.drawText(size[0] / 2, yy, t, self.textOpts["size"], "yellow")
            y += 32
        gfx.restore()


class FrameGame(Frame):
    game = Game()
    greyed = False

    def onEnter(self):
        _ = self
        _.game.newGame()
        self.textOpts["align"] = "center"
        gameState.countDown = 10
        gameState.player.ai = True
        gameState.player.indestructible = True
        # for s in gameState.track.segments:
        #     s.color = "Red"
        self.opts["track"] = True
        self.opts["rail"] = True
        self.opts["border"] = True
        self.opts["section_track"] = True
        self.opts["section_rail"] = True

    def onUpdate(self, dt):
        self.game.update(dt)

        if self.ticks > 2000:
            self.text = "Building an Endless Racing Game"
            self.textOpts["size"] = 3
        if self.ticks > 8000:
            self.text = ""
            self.greyed = True

    def onRender(self, gfx):
        _ = self

        player = gameState.player
        track = gameState.track

        size = [gameState.screenWidth, gameState.screenHeight]
        gfx.save()

        if self.greyed:
            gfx.state.forcedColor = "Grey62"

        # camera
        scale = self.opts["scale"] - (50 * player.speed / 1)
        gfx.scale(scale, scale)
        cam = gfx.transform(
            Vector.copy(player.pos).add(
                Vector.copy(player.direction).scale(
                    player.radius * 3 + (player.radius * player.speed)
                )
            )
        )
        if gameState.cam != None:
            cam.scale(4).add(gameState.cam).scale(1 / 5)
        gameState.cam = Vector.copy(cam)
        gfx.translate(size[0] / 2 - cam.x, size[1] / 2 - cam.y)

        renderTrack(gfx, track.segments[0], gameState.player, self.opts)

        for t in entityService.entities:
            for e in entityService.entities[t]:
                opt = {}
                if not e.type in [EntityType.particle, EntityType.explosion]:
                    opt = {
                        "entityVectors": _.opts["entityVectors"],
                        "steerAssist": _.opts["steerAssist"],
                    }
                Renderer.renderEntity(gfx, e, opt)

        gfx.restore()

        Frame.onRender(self, gfx)


class FrameGame2(FrameGame):
    def onEnter(self):
        FrameGame.onEnter(self)
        self.text = "Combine all these and now we\nhave an endless random race track"
        self.textOpts["align"] = "bottom"

    def onUpdate(self, dt):
        self.game.update(dt)

        if self.ticks > 6000:
            self.text = "Objects are randomly be attached at\nvarious track points"


class FrameGame3(FrameGame):
    def onEnter(self):
        FrameGame.onEnter(self)
        gameState.player.max_speed = 0.4
        self.text = ""
        self.opts["scale"] = 120
        self.textOpts["align"] = "bottom"

    def onUpdate(self, dt):
        self.game.update(dt)
        if self.ticks > 4000:
            self.text = "Ships are assigned a radius used for\ncollision detection with other objects"
            self.opts["entityVectors"] = True
        if self.ticks > 10000:
            self.text = "They have a speed vector"
        if self.ticks > 14000:
            self.text = "And a direction vector"
            # self.opts["steerAssist"] = True
        if self.ticks > 18000:
            self.text = "These are affected by player or AI input.\nAnd interpolates the ship position over time."
        if self.ticks > 26000:
            self.text = "The track also has collision points as barriers"
            self.opts["collisionPoints"] = True
            self.opts["section_track"] = False
            self.opts["section_rail"] = False
            # self.opts["steerAssist"] = False


class FrameGame4(FrameGame):
    def onEnter(self):
        FrameGame.onEnter(self)
        gameState.player.max_speed = 0.4
        gameState.player.shape = ships["objects"]["ship_2"]
        self.text = ""
        self.opts["scale"] = 120
        self.textOpts["align"] = "bottom"

    def onUpdate(self, dt):
        self.game.update(dt)
        if self.ticks > 2000:
            self.text = "The AI simply updates its direction vector\nto follow the center racing line."
            self.opts["entityVectors"] = True
        if self.ticks > 4000:
            self.opts["steerAssist"] = True
        if self.ticks > 8000:
            self.text = "They throttle down at sharp turns"
        if self.ticks > 13000:
            self.text = ""
        if self.ticks > 14500:
            self.text = "They are determined to outrace you"
            self.opts["entityVectors"] = False
            self.opts["steerAssist"] = False
        if self.ticks > 18500:
            self.text = ""
            self.greyed = True


class FrameGame5(FrameGame):
    def onEnter(self):
        FrameGame.onEnter(self)
        self.game.countDown = 6000
        self.game.addOtherShips()
        self.text = "Enjoy the game!!"
        self.textOpts["align"] = "bottom"
        self.opts["scale"] = 120

    def onUpdate(self, dt):
        self.game.update(dt)
        if self.ticks > 7000:
            self.text = "Enjoy the game"
        if self.ticks > 12000:
            self.text = ""


class FrameTrack(Frame):
    segments = None
    wait = 0

    def prepSegment(self):
        pass

    def onEnter(self):
        self.opts["scale"] = 50
        self.segments = []

    def onUpdate(self, dt):
        if self.wait == 0:
            self.prepSegment()

        self.wait += dt
        if self.wait > 2000:
            self.wait = 0

    def onRender(self, gfx):
        size = [gameState.screenWidth, gameState.screenHeight]

        gfx.save()

        # camera
        segments = self.segments
        midSegment = Floor(len(segments) / 2)
        targetSegment = segments[midSegment]
        mid = Floor(len(targetSegment.trackPoints) / 2)
        targetPoint = targetSegment.trackPoints[mid].point

        scale = self.opts["scale"]
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
                self.opts,
            )

        gfx.restore()
        Frame.onRender(self, gfx)


class FrameLines(FrameTrack):
    track = None

    def prepSegment(self):
        self.text = "Start by creating random lines"
        self.textOpts["align"] = "bottom"
        self.opts["line"] = True
        track = TrackGenerator()
        self.track = track
        track.addSector([TrackSegment.randomLineSegment()])
        track.segments[0].baseAngle = Rand(0, 360)
        track.compute()
        self.segments = track.segments


class FrameLinesExpand(FrameLines):
    def prepSegment(self):
        FrameLines.prepSegment(self)
        self.track.segments[0].length = 12
        self.track.segments[0].trackWidth = 2
        self.track.compute()
        self.opts["scale"] = 80
        self.text = "Expand the segment with a track width\nby extruding points and forming outer lines"
        if self.ticks > 3000:
            self.opts["track"] = True
        if self.ticks > 7000:
            self.opts["rail"] = True
            self.text = "The outer lines are parallel to the racing line"
        if self.ticks > 13000:
            self.opts["border"] = True
            self.text = "Extrude more points for more details"
        if self.ticks > 17000:
            self.opts["section_track"] = True
            self.text = ""
            self.opts["line"] = False
        if self.ticks > 21000:
            self.opts["section_rail"] = True
            self.text = ""


class FrameArcs(FrameTrack):
    track = None

    def prepSegment(self):
        self.text = "And random arcs"
        self.textOpts["align"] = "bottom"
        self.opts["line"] = True
        track = TrackGenerator()
        self.track = track
        track.addSector([TrackSegment.randomArcSegment()])
        track.segments[0].baseAngle = Rand(0, 360)
        track.compute()
        self.segments = track.segments


class FrameArcsExpand(FrameArcs):
    def prepSegment(self):
        FrameArcs.prepSegment(self)
        self.text = ""
        self.track.segments[0].length = 8
        self.track.segments[0].trackWidth = 2
        self.track.compute()
        if self.ticks > 3000:
            self.opts["track"] = True
        if self.ticks > 6000:
            self.opts["rail"] = True
        if self.ticks > 90000:
            self.opts["border"] = True
        if self.ticks > 12000:
            self.opts["section_track"] = True
            self.opts["section_rail"] = True
            self.opts["line"] = False


class FrameLinesAndArcs(FrameTrack):
    def prepSegment(self):
        self.text = "Combine these and you have random track features"
        self.textOpts["align"] = "bottom"
        self.opts["line"] = True
        self.opts["scale"] = 20
        track = TrackGenerator()
        track.addSector(
            [
                TrackSegment.randomArcSegment(),
                TrackSegment.randomLineSegment(),
                TrackSegment.randomArcSegment(),
                TrackSegment.randomLineSegment(),
            ]
        )
        track.segments[0].baseAngle = Rand(0, 360)
        track.compute()
        self.segments = track.segments


class FrameFeatures(FrameTrack):
    track = None

    def prepSegment(self):
        self.text = ""
        self.textOpts["align"] = "bottom"
        track = TrackGenerator()
        self.track = track

        self.opts["track"] = True
        self.opts["line"] = False
        self.opts["scale"] = 40

        if self.ticks < 3000:
            track.addSector(track.defs["angle"][0].copySegments())
            self.text = "Sharp turns"
        elif self.ticks < 6000:
            track.addSector(track.defs["angle"][1].copySegments())
            self.text = "Sharp turns"
        elif self.ticks < 9000:
            track.addSector(track.defs["chicane"][0].copySegments())
            self.text = "Chicanes"
        elif self.ticks < 12000:
            track.addSector(track.defs["chicane"][0].copySegments())
            self.text = "Chicanes"
        elif self.ticks < 15000:
            track.addSector(track.defs["loop"][0].copySegments())
            self.text = "Loops"
        elif self.ticks < 18000:
            track.addSector(track.defs["loop"][0].copySegments())
            self.text = "Loops"
        else:
            track.addSector(track.randomSector(0))
            track.addSector(track.randomSector(0))
            track.addSector(track.randomSector(0))
            self.text = ""

        track.segments[0].baseAngle = Rand(0, 360)
        track.compute()
        self.segments = track.segments


class DemoScene(Scene):
    ticks = 0
    track = TrackGenerator()
    frames = []

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
            if not f.entered:
                f.onEnter()
                f.entered = True
            f.ticks += dt
            f.onUpdate(dt)

        _.ticks += dt

    def onRender(self, gfx):
        _ = self
        track = _.track

        gfx.save()
        gfx.clear("black")

        frames = _.getFrames(_.ticks)
        for f in frames:
            if f.entered:
                f.onRender(gfx)

        gfx.restore()

    def onEnter(self):
        _ = self
        _.ticks = 0
        _.frames = []
        _.frames.append(Frame(2000))
        _.frames.append(FrameGame(10000))
        _.frames.append(
            Frame(5000, "Create random racing lines", None, {"align": "center"})
        )
        _.frames.append(FrameLines(6000))
        _.frames.append(FrameArcs(6000))
        _.frames.append(FrameLinesAndArcs(10000))
        _.frames.append(FrameLinesExpand(22000))
        _.frames.append(FrameArcsExpand(14000))
        _.frames.append(
            Frame(5000, "Some track features are handmade", None, {"align": "center"})
        )
        _.frames.append(FrameFeatures(22000))
        _.frames.append(FrameGame2(24000))
        _.frames.append(Frame(5000, "Physics of the game", None, {"align": "center"}))
        _.frames.append(FrameGame3(32000))
        _.frames.append(Frame(5000, "AI Enemies", None, {"align": "center"}))
        _.frames.append(FrameGame4(22000))
        _.frames.append(
            Frame(
                8000,
                "This game is an homage to Sony's legendary\nWipeout Pure (Zone Mode)",
                None,
                {"align": "center"},
            )
        )
        _.frames.append(FrameGame5(60000))
