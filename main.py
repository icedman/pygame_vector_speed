import pygame
import sys

from maths import *
from draw import Context
from renderer import *
from game import *
from track import *
from colors import tint, untint
from sounds import *
from scene import *
from demo import *


pygame.init()

# setup sounds
soundService.defs[Effects.mines] = pygame.mixer.Sound("./sounds/draven/spawn/d1.wav")
soundService.defs[Effects.countDown] = pygame.mixer.Sound(
    "./sounds/sounds/buttonselect/1.wav"
)
soundService.defs[Effects.bump] = pygame.mixer.Sound("./sounds/sounds/laserd.wav")
soundService.defs[Effects.speedpad] = pygame.mixer.Sound("./sounds/draven/spawn/d5.wav")
soundService.defs[Effects.powerup] = pygame.mixer.Sound(
    "./sounds/jalastram/powerup.mp3"
)
soundService.defs[Effects.explosion] = pygame.mixer.Sound("./sounds/draven/bomb.wav")
pygame.mixer.music.load("./sounds/f16-fighter-jet-start-upaif-14690.mp3")
pygame.mixer.music.set_volume(0)

for d in soundService.defs:
    soundService.defs[d].set_volume(0.25)

gameState.trackedKeys = {
    pygame.K_UP: "up",
    pygame.K_DOWN: "down",
    pygame.K_LEFT: "left",
    pygame.K_RIGHT: "right",
    pygame.K_ESCAPE: "escape",
    pygame.K_SPACE: " ",
    pygame.K_w: "w",
    pygame.K_a: "a",
    pygame.K_s: "s",
    pygame.K_d: "d",
    pygame.K_p: "p",  # pause
    pygame.K_t: "t",  # toggle sound
    pygame.K_o: "o",  # demo
    pygame.K_l: "l",  # demo
    pygame.K_i: "i",  # demo
}
gameState.init()

# size = [1600, 900]
size = [1280, 800]
screen = pygame.display.set_mode(size)
gfx = Context(screen)
gfx.state.strokeWidth = 1

game = Game()
game.setup(size)
log = []


def print_log(t):
    log.append(t)


def cull(v1, v2):
    w = size[0]
    h = size[1]
    if (v1.x < 0 and v2.x < 0) or (v1.y < 0 and v2.y < 0):
        return True
    if (v1.x > w and v2.x > w) or (v1.y > h and v2.y > h):
        return True
    return False


gfx.cull = cull


def toggleTint():
    gameState.tinted = not gameState.tinted
    if gameState.tinted:
        tint(0, 255, 0, 0.6)
    else:
        untint()


class GameScene(Scene):
    type = SceneType.game
    showHud = True

    def onEnter(self):
        game.newGame(777)
        game.addOtherShips()
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)

    def onExit(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

    def onUpdate(self, dt):
        player = gameState.player
        track = gameState.track

        pressed = gameState.pressed
        if pressed["left"] or pressed["a"]:
            player.steerLeft()
        if pressed["right"] or pressed["d"]:
            player.steerRight()
        if pressed["up"] or pressed["w"]:
            player.throttleUp()
        if pressed["down"] or pressed["s"]:
            player.throttleDown()

        if gameState.released["escape"]:
            sceneService.enterScene(SceneType.menu)
            return
        if gameState.released[" "] and gameState.gameOver:
            sceneService.enterScene(SceneType.menu)
            return

        game.update(dt)

        # sound effects
        for r in soundService.requests:
            cnt = soundService.requests[r]
            del soundService.requests[r]
            snd = soundService.defs[r]
            pygame.mixer.Sound.stop(snd)
            pygame.mixer.Sound.play(snd)
            break

        # music
        v = gameState.player.speed
        if v > 1:
            v = 1
        pygame.mixer.music.set_volume(v)

    def onRender(self, gfx):
        player = gameState.player
        track = gameState.track

        gfx.clear("black")
        gfx.save()

        # camera
        scale = 90 - (50 * player.speed / 1)
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

        renderTrack(gfx, track.segments[0], gameState.player)

        for t in entityService.entities:
            for e in entityService.entities[t]:
                Renderer.renderEntity(gfx, e)

        gfx.restore()

        if self.showHud:
            render_hud(gfx, gameState, print_log)
            render_minimap(gfx, gameState, print_log)


class MenuScene(GameScene):
    type = SceneType.menu

    def onEnter(self):
        self.showHud = False
        game.newGame(888)
        gameState.countDown = 2000
        gameState.player.ai = True
        gameState.player.indestructible = True

    def onUpdate(self, dt):
        if gameState.released[" "]:
            sceneService.enterScene(SceneType.game)
            return
        if gameState.released["escape"]:
            gameState.done = True
            return

        game.update(dt)

    def onRender(self, gfx):
        player = gameState.player
        track = gameState.track

        gfx.saveAttributes()
        gfx.state.forcedColor = "Grey23"
        GameScene.onRender(self, gfx)
        gfx.restore()

        gfx.drawRect(0, 0, size[0], size[1], "red")
        gfx.save()

        gfx.saveAttributes()
        gfx.state.strokeWidth = 4
        gfx.drawText(size[0] / 2, size[1] / 2, "Vector Speed AG", 4, "yellow")
        gfx.restore()
        gfx.drawText(size[0] / 2, size[1] / 2 + 150, "Press SPACE to play", 1.5, "red")
        gfx.drawText(
            size[0] / 2, size[1] / 2 + 150 + 30, "Press T to toggle colors", 1, "red"
        )
        gfx.drawText(
            size[0] / 2, size[1] - 120 + 0, "A, D, Left, Right to steer", 1, "white"
        )
        gfx.drawText(
            size[0] / 2,
            size[1] - 120 + 25,
            "W, S, Up, Down to control speed",
            1,
            "white",
        )

        gfx.restore()


sceneService.defs[SceneType.menu] = MenuScene()
sceneService.defs[SceneType.game] = GameScene()
sceneService.defs[SceneType.demo] = DemoScene()
sceneService.enterScene(SceneType.menu)

for arg in sys.argv:
    if arg.startswith("-"):
        gameState.pressed[arg[1:]] = True

rendered = 0
last_tick = 0
while not gameState.done:
    tick = pygame.time.get_ticks()
    dt = tick - last_tick
    if dt < 16:
        continue
    last_tick = tick

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameState.done = True

    pressed = pygame.key.get_pressed()
    for k in gameState.trackedKeys:
        hk = gameState.trackedKeys[k]
        gameState.released[hk] = gameState.pressed[hk] == True and pressed[k] == False
        gameState.pressed[hk] = pressed[k]

    if gameState.released["p"]:
        gameState.paused = not gameState.paused
    if gameState.paused:
        continue
    if gameState.released["t"]:
        toggleTint()
    if gameState.released["o"]:
        sceneService.enterScene(SceneType.demo)
    if gameState.released["l"]:
        gfx.basicDraw = not gfx.basicDraw
    if gameState.released["i"]:
        gameState.showFps = not gameState.showFps

    sceneService.current.onUpdate(dt)
    sceneService.current.onRender(gfx)

    row = 0
    for l in log:
        gfx.drawText(25, 50 + row * 24, l, 1.5, "cyan", 1)
        row += 1
    log = []

    if gameState.showFps:
        rendered += 1
        if rendered > 0:
            fps = "{}fps".format(Floor(rendered * 1000 / last_tick))
            gfx.drawText(size[0] - 100, 40, fps, 2, "red")

    pygame.display.flip()
