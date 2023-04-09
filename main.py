import pygame
from maths import *
from draw import Context
from renderer import *
from game import *
from track import *
from generator import *
from colors import tint, untint
from sounds import *

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
    pygame.K_p: "p",
    pygame.K_t: "t",
}
gameState.init()

game = Game()
def generate_meter(x, y):
    t = TrackGenerator()
    t.addSector([
        TrackSegment.randomArcSegment(),
        TrackSegment.randomLineSegment(),
    ])
    t.segments[0].segmentType = TrackSegmentType.ARC_LEFT
    t.segments[0].baseAngle = -45
    t.segments[0].arc = 45
    t.segments[0].radius = 0.1
    t.segments[0].startRadius = 0.1
    t.segments[0].endRadius = 0.08
    t.segments[1].length = 8
    t.compute(0)

    res = []
    m = Matrix.identity().scale(20, 20, 1)
    m.multiply(Matrix.identity().translate(x, y, 0))
    tp = t.segments[0].trackPoints[0]
    while tp != None:
        v = Vector.copy(tp.point).transform(m)
        res.append([v.x, v.y])
        nextTp = TrackPoint.advance(tp, 1)
        if nextTp == tp:
            break
        tp = nextTp

    return res

meter = generate_meter(0, 0)

# tint(0, 255, 0, 0.6)
# gameState.tinted = True

# tint(255, 0, 0, 0.6)

# size = [1600, 900]
size = [1280, 800]
screen = pygame.display.set_mode(size)
done = False
gfx = Context(screen)
gfx.state.strokeWidth = 1

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


def enter_scene(scn):
    gameState.scene = scn
    if gameState.scene == 0:
        game.newGame(888)
        gameState.countDown = 2000
        gameState.player.ai = True
        gameState.player.indestructible = True
    elif gameState.scene == 1:
        game.newGame(777)


def toggleTint():
    gameState.tinted = not gameState.tinted
    if gameState.tinted:
        tint(0, 255, 0, 0.6)
    else:
        untint()


def game_loop(dt):
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

    game.update(dt)

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


def menu_loop(dt):
    if gameState.released[" "]:
        enter_scene(1)

    gfx.clear("black")
    gfx.saveAttributes()
    gfx.state.forcedColor = "Grey23"
    game_loop(dt)
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
        size[0] / 2, size[1] - 120 + 25, "W, S, Up, Down to control speed", 1, "white"
    )
    # gfx.drawText(size[0] / 2, size[1] - 120 + 50, "Space to explode bomb", 1, "white")

    gfx.restore()


def render_hud(dt):
    player = gameState.player
    track = gameState.track

    if gameState.gameOver:
        gfx.drawText(size[0] / 2, size[1] / 2, "Game Over", 2, "red")

    # count down
    if gameState.countDown > 0:
        gfx.saveAttributes()
        c = Floor(gameState.countDown / 1200)
        cd = gameState.countDown / 1200
        cs = "{}".format(c)
        if cd - c < 0.30:
            cs = ""
        if gameState.lastCount != c and c <= 3:
            soundService.play(Effects.countDown)
            gameState.lastCount = c
        if c <= 3:
            if c == 0:
                cs = "GO"
            gfx.state.strokeWidth = 6
            pos = [size[0] / 2, size[1] / 2]
            gfx.drawText(pos[0], pos[1], cs, 6, "yellow")
        gfx.restore()
        return

    # race position
    gfx.saveAttributes()

    # race position
    pos = [size[0] - 110, size[1] - 90]
    gfx.state.strokeWidth = 4
    gfx.drawText(pos[0], pos[1], "{}/".format(player.race_position), 2.5, "yellow", 1)
    gfx.state.strokeWidth = 2
    gfx.drawText(
        pos[0] + 48, pos[1] + 10, "3".format(player.race_position), 2, "yellow", 1
    )

    # travel
    pos = [40, size[1] - 100]
    gfx.state.strokeWidth = 3
    gfx.drawText(pos[0], pos[1], "{}".format(Floor(player.travel)), 2, "white", 1)

    # time
    pos = [40, size[1] - 60]
    tick = gameState.tick
    mins = Floor(tick / (1000 * 60))
    tick -= mins * 1000 * 60
    secs = Floor(tick / (1000))
    tick -= secs * 1000
    millis = Floor(tick)
    gfx.state.strokeWidth = 2
    gfx.drawText(
        pos[0],
        pos[1],
        "{:02d}:{:02d}:{:03d}".format(mins, secs, millis),
        1.5,
        "yellow",
        1,
    )

    # meters
    l = len(meter)
    gfx.save()
    gfx.state.strokeWidth = 8
    # speed
    pos = [size[0]-240, size[1]-30]
    gfx.translate(pos[0], pos[1])
    gfx.drawPolygonPoints(meter, "white", False)
    sp = gameState.player.speed / gameState.player.max_speed
    mm = []
    for i in range(0, Floor(l*sp)):
        mm.append(meter[i])
    gfx.drawPolygonPoints(mm, "cyan", False)
    # shield
    pos = [10, 20]
    gfx.translate(pos[0], pos[1])
    gfx.drawPolygonPoints(meter, "white", False)
    sp = gameState.player.shield / gameState.player.max_shield
    color = "green"
    if sp < 0.1:
        color = "red"
        if gameState.player.shield <= 0:
            print_log("ship disabled")
        else:
            print_log("warning")
    mm = []
    for i in range(0, Floor(l*sp)):
        mm.append(meter[i])
    gfx.drawPolygonPoints(mm, color, False)
    gfx.restore()

    if player.boost_t > 0:
        print_log("boost")
    if player.damage_t > 0:
        print_log("damage")

    gfx.restore()


enter_scene(0)
gameState.countDown = 0

paused = False
last_tick = 0
while not done:
    tick = pygame.time.get_ticks()
    dt = tick - last_tick
    if dt < 16:
        continue
    last_tick = tick

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pressed = pygame.key.get_pressed()
    for k in gameState.trackedKeys:
        hk = gameState.trackedKeys[k]
        gameState.released[hk] = gameState.pressed[hk] == True and pressed[k] == False
        gameState.pressed[hk] = pressed[k]

    if gameState.released["p"]:
        paused = not paused
    if gameState.released["t"]:
        toggleTint()
    if gameState.released[" "] and gameState.gameOver:
        enter_scene(0)

    if paused:
        continue

    if gameState.scene == 0:
        menu_loop(dt)
        if gameState.released["escape"]:
            done = True

    elif gameState.scene == 1:
        if gameState.released["escape"]:
            enter_scene(0)
            continue
        game_loop(dt)
        render_hud(dt)

    row = 0
    for l in log:
        gfx.drawText(25, 50 + row * 24, l, 1.5, "cyan", 1)
        row += 1
    log = []

    pygame.display.flip()

    for r in soundService.requests:
        cnt = soundService.requests[r]
        del soundService.requests[r]
        snd = soundService.defs[r]
        pygame.mixer.Sound.stop(snd)
        pygame.mixer.Sound.play(snd)
        break
