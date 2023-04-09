class GameState:
    scene = 0
    screenWidth = 0
    screenHeight = 0
    gameOver = False
    tick = 0

    screen = {"width": 1024, "height": 768}
    keys = {
        "w": False,
        "a": False,
        "s": False,
        "d": False,
        "left": False,
        "right": False,
        "up": False,
        "down": False,
        "p": False,
        " ": False,
    }
    last_pressed = []
    player = None
    powers = {}

    def init(self):
        self.gameOver = False
        self.tick = 0
        self.keys = {
            "w": False,
            "a": False,
            "s": False,
            "d": False,
            "left": False,
            "right": False,
            "up": False,
            "down": False,
            "p": False,
            " ": False,
        }
        self.last_pressed = []
        self.player = None
        self.powers = {}


gameState = GameState()
