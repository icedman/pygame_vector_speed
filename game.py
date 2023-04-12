from maths import *
from state import gameState
from track import *
from generator import *

from entity import *
from ship import *
from particles import *
from ship import *
from powerup import *
from state import *


class Game:
    def setup(self, size):
        gameState.screenWidth = size[0]
        gameState.screenHeight = size[1]
        self.newGame()

    def newGame(self, retainState=False, seed=None):
        if seed != None:
            random.seed(seed)

        gameState.init()
        self.clear()

        track = TrackGenerator()
        track.buildStart()
        gameState.track = track

        player = entityService.attach(entityService.create(EntityType.ship))
        gameState.player = player

        track.attachToStartingGrid(player)

    def addOtherShips(self):
        track = gameState.track

        enemy1 = entityService.attach(entityService.create(EntityType.enemyShip))
        enemy1.setGraphics("ship_2")
        track.attachToStartingGrid(enemy1, 2)

        enemy2 = entityService.attach(entityService.create(EntityType.enemyShip))
        enemy2.setGraphics("ship_1")
        track.attachToStartingGrid(enemy2, 4)

    def clear(self):
        entityService.init()

    def resetGame(self):
        return

    def update(self, dt):
        if gameState.countDown > 0:
            gameState.countDown -= dt
            return

        if gameState.gameOver != True:
            gameState.tick += dt

        track = gameState.track
        player = gameState.player

        entityService.update(dt)

        if player.segment != None:
            track.buildSector(player.segment.sector, 2, 4)
            track.prune(player.segment.sector, 4)
