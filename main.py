import pygame
from maths import *
from draw import Context
from renderer import *
from game import *
from colors import tint, untint

gameState.trackedKeys = {
    pygame.K_UP: "up",
    pygame.K_DOWN: "down",
    pygame.K_LEFT: "left",
    pygame.K_RIGHT: "right",
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

# tint(0, 255, 0, 0.6)
# gameState.tinted = True

# tint(255, 0, 0, 0.6)

pygame.init()
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

    # count down
    if gameState.countDown > 0:
        gfx.saveAttributes()
        c = Floor(gameState.countDown / 1200)
        cd = gameState.countDown / 1200
        cs = "{}".format(c)
        if cd - c < 0.30:
            cs = ""
        if c <= 3:
            if c == 0:
                cs = "GO"
            gfx.state.strokeWidth = 6
            pos = [size[0] / 2, size[1] / 2]
            gfx.drawText(pos[0], pos[1], cs, 6, "yellow")
        gfx.restore()
        return

    if player.boost_t > 0:
        print_log("boost")
    if player.damage_t > 0:
        print_log("damage")

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
    gfx.drawText(pos[0], pos[1], "{}".format(Floor(player.travel)), 2, "yellow", 1)

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

    gfx.restore()


enter_scene(0)

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
    if pressed[pygame.K_ESCAPE]:
        done = True

    for k in gameState.trackedKeys:
        hk = gameState.trackedKeys[k]
        gameState.released[hk] = gameState.pressed[hk] == True and pressed[k] == False
        gameState.pressed[hk] = pressed[k]

    if gameState.released["p"]:
        paused = not paused
    if gameState.released["t"]:
        toggleTint()

    if paused:
        continue

    if gameState.scene == 0:
        menu_loop(dt)
    elif gameState.scene == 1:
        game_loop(dt)
        render_hud(dt)

    row = 0
    for l in log:
        gfx.drawText(25, 50 + row * 24, l, 1.5, "yellow", 1)
        row += 1
    log = []

    pygame.display.flip()
