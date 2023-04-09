import pygame
from maths import *
from draw import Context
from track import *
from generator import *
from renderer import *
from entity import *
from particles import *
from ship import *
from powerup import *
from state import *
from game import *

game = Game()
game.newGame()

track = TrackGenerator()
track.buildStart()

pygame.init()
# size = [1600, 900]
size = [1280, 800]
screen = pygame.display.set_mode(size)
done = False
gfx = Context(screen)
gfx.state.strokeWidth = 1


def cull(v1, v2):
    w = size[0]
    h = size[1]
    if (v1.x < 0 and v2.x < 0) or (v1.y < 0 and v2.y < 0):
        return True
    if (v1.x > w and v2.x > w) or (v1.y > h and v2.y > h):
        return True
    return False


gfx.cull = cull

trackKeys = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
keys = {}
released = {}

obj = entityService.attach(entityService.create(EntityType.ship))
obj.radius = 0.3
obj.track = track
track.addToStartingGrid(obj)
gameState.player = obj

# entityService.attach(entityService.create(EntityType.powerUp, obj.pos.x, obj.pos.y))
# entityService.createFloatingText(obj.pos.x, obj.pos.y, "+20")

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

    for k in trackKeys:
        released[k] = k in keys and keys[k] == True and pressed[k] == False
        keys[k] = pressed[k]

    if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
        obj.steerLeft()
    if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
        obj.steerRight()
    if pressed[pygame.K_UP] or pressed[pygame.K_w]:
        obj.throttleUp()
    if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
        obj.throttleDown()

    entityService.update(dt)
    if obj.segment != None:
        track.buildSector(obj.segment.sector, 2, 4)
        track.prune(obj.segment.sector, 4)

    gfx.clear("black")
    gfx.save()
    gfx.drawRect(0, 0, size[0], size[1], "red")

    scale = 90 - (40 * obj.speed / 1)
    gfx.scale(scale, scale)

    # camera
    cam = gfx.transform(
        Vector.copy(obj.pos).add(
            Vector.copy(obj.direction).scale(obj.radius * 3 + (obj.radius * obj.speed))
        )
    )
    gfx.translate(size[0] / 2 - cam.x, size[1] / 2 - cam.y)

    renderTrack(gfx, track.segments[0], gameState.player)

    for t in entityService.entities:
        for e in entityService.entities[t]:
            Renderer.renderEntity(gfx, e)

    gfx.restore()

    pygame.display.flip()
