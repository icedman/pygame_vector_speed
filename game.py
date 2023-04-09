from maths import *
from entity import *
from state import gameState


class Game:
    def setup(self, size):
        gameState.screenWidth = size[0]
        gameState.screenHeight = size[1]
        self.newGame()

    def newGame(self, retainState=False):
        return

    def clear(self):
        entityService.init()

    def resetGame(self):
        return

    def update(self, dt):
        return
