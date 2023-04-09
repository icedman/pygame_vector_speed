class GameState:
    scene = 0
    screenWidth = 0
    screenHeight = 0
    gameOver = False
    tick = 0
    countDown = 0

    screen = {"width": 1024, "height": 768}
    trackedKeys = {}
    pressed = {}
    released = {}
    player = None
    track = None

    cam = None
    tinted = False

    def init(self):
        _ = self
        _.gameOver = False
        _.tick = 0
        _.pressed = {}
        _.released = {}
        _.player = None
        _.track = None
        _.cam = None
        _.countDown = 6000
        for k in _.trackedKeys:
            _.pressed[_.trackedKeys[k]] = False
            _.released[_.trackedKeys[k]] = False


gameState = GameState()
