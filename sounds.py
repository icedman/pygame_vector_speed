from enum import Enum


class Effects(Enum):
    none = 0
    bump = 1
    powerup = 2
    speedpad = 3
    explosion = 4
    countDown = 5
    mines = 6


class Sounds:
    defs = {}
    requests = {}

    def play(self, s):
        if not s in self.defs:
            return
        if not s in self.requests:
            self.requests[s] = 0
        self.requests[s] += 1


soundService = Sounds()
