FONT_UP = 0xFE
FONT_LAST = 0xFF

fnt = {}


def P(x, y):
    return (((x) & 0xF) << 4) | (((y) & 0xF) << 0)


def C(c):
    return ord(c)


fnt[ord("0") - 0x20] = [
    P(0, 0),
    P(8, 0),
    P(8, 12),
    P(0, 12),
    P(0, 0),
    P(8, 12),
    FONT_LAST,
]
fnt[ord("1") - 0x20] = [P(4, 0), P(4, 12), P(3, 10), FONT_LAST]
fnt[ord("2") - 0x20] = [
    P(0, 12),
    P(8, 12),
    P(8, 7),
    P(0, 5),
    P(0, 0),
    P(8, 0),
    FONT_LAST,
]
fnt[ord("3") - 0x20] = [
    P(0, 12),
    P(8, 12),
    P(8, 0),
    P(0, 0),
    FONT_UP,
    P(0, 6),
    P(8, 6),
    FONT_LAST,
]
fnt[ord("4") - 0x20] = [
    P(0, 12),
    P(0, 6),
    P(8, 6),
    FONT_UP,
    P(8, 12),
    P(8, 0),
    FONT_LAST,
]
fnt[ord("5") - 0x20] = [
    P(0, 0),
    P(8, 0),
    P(8, 6),
    P(0, 7),
    P(0, 12),
    P(8, 12),
    FONT_LAST,
]
fnt[ord("6") - 0x20] = [P(0, 12), P(0, 0), P(8, 0), P(8, 5), P(0, 7), FONT_LAST]
fnt[ord("7") - 0x20] = [P(0, 12), P(8, 12), P(8, 6), P(4, 0), FONT_LAST]
fnt[ord("8") - 0x20] = [
    P(0, 0),
    P(8, 0),
    P(8, 12),
    P(0, 12),
    P(0, 0),
    FONT_UP,
    P(0, 6),
    P(8, 6),
]
fnt[ord("9") - 0x20] = [P(8, 0), P(8, 12), P(0, 12), P(0, 7), P(8, 5), FONT_LAST]
fnt[ord(" ") - 0x20] = [FONT_LAST]
fnt[ord(".") - 0x20] = [P(3, 0), P(4, 0), FONT_LAST]
fnt[ord(",") - 0x20] = [P(2, 0), P(4, 2), FONT_LAST]
fnt[ord("-") - 0x20] = [P(2, 6), P(6, 6), FONT_LAST]
fnt[ord("+") - 0x20] = [P(1, 6), P(7, 6), FONT_UP, P(4, 9), P(4, 3), FONT_LAST]
fnt[ord("!") - 0x20] = [
    P(4, 0),
    P(3, 2),
    P(5, 2),
    P(4, 0),
    FONT_UP,
    P(4, 4),
    P(4, 12),
    FONT_LAST,
]
fnt[ord("#") - 0x20] = [
    P(0, 4),
    P(8, 4),
    P(6, 2),
    P(6, 10),
    P(8, 8),
    P(0, 8),
    P(2, 10),
    P(2, 2),
]
fnt[ord("^") - 0x20] = [P(2, 6), P(4, 12), P(6, 6), FONT_LAST]
fnt[ord("=") - 0x20] = [P(1, 4), P(7, 4), FONT_UP, P(1, 8), P(7, 8), FONT_LAST]
fnt[ord("*") - 0x20] = [
    P(0, 0),
    P(4, 12),
    P(8, 0),
    P(0, 8),
    P(8, 8),
    P(0, 0),
    FONT_LAST,
]
fnt[ord("_") - 0x20] = [P(0, 0), P(8, 0), FONT_LAST]
fnt[ord("/") - 0x20] = [P(0, 0), P(8, 12), FONT_LAST]
fnt[ord("\\") - 0x20] = [P(0, 12), P(8, 0), FONT_LAST]
fnt[ord("@") - 0x20] = [
    P(8, 4),
    P(4, 0),
    P(0, 4),
    P(0, 8),
    P(4, 12),
    P(8, 8),
    P(4, 4),
    P(3, 6),
]
fnt[ord("$") - 0x20] = [
    P(6, 2),
    P(2, 6),
    P(6, 10),
    FONT_UP,
    P(4, 12),
    P(4, 0),
    FONT_LAST,
]
fnt[ord("&") - 0x20] = [
    P(8, 0),
    P(4, 12),
    P(8, 8),
    P(0, 4),
    P(4, 0),
    P(8, 4),
    FONT_LAST,
]
fnt[ord("[") - 0x20] = [P(6, 0), P(2, 0), P(2, 12), P(6, 12), FONT_LAST]
fnt[ord("]") - 0x20] = [P(2, 0), P(6, 0), P(6, 12), P(2, 12), FONT_LAST]
fnt[ord("(") - 0x20] = [P(6, 0), P(2, 4), P(2, 8), P(6, 12), FONT_LAST]
fnt[ord(")") - 0x20] = [P(2, 0), P(6, 4), P(6, 8), P(2, 12), FONT_LAST]
fnt[ord("{") - 0x20] = [
    P(6, 0),
    P(4, 2),
    P(4, 10),
    P(6, 12),
    FONT_UP,
    P(2, 6),
    P(4, 6),
    FONT_LAST,
]
fnt[ord("}") - 0x20] = [
    P(4, 0),
    P(6, 2),
    P(6, 10),
    P(4, 12),
    FONT_UP,
    P(6, 6),
    P(8, 6),
    FONT_LAST,
]
fnt[ord("%") - 0x20] = [
    P(0, 0),
    P(8, 12),
    FONT_UP,
    P(2, 10),
    P(2, 8),
    FONT_UP,
    P(6, 4),
    P(6, 2),
]
fnt[ord("<") - 0x20] = [P(6, 0), P(2, 6), P(6, 12), FONT_LAST]
fnt[ord(">") - 0x20] = [P(2, 0), P(6, 6), P(2, 12), FONT_LAST]
fnt[ord("|") - 0x20] = [P(4, 0), P(4, 5), FONT_UP, P(4, 6), P(4, 12), FONT_LAST]
fnt[ord(":") - 0x20] = [P(4, 9), P(4, 7), FONT_UP, P(4, 5), P(4, 3), FONT_LAST]
fnt[ord(";") - 0x20] = [P(4, 9), P(4, 7), FONT_UP, P(4, 5), P(1, 2), FONT_LAST]
fnt[ord('"') - 0x20] = [P(2, 10), P(2, 6), FONT_UP, P(6, 10), P(6, 6), FONT_LAST]
fnt[ord("'") - 0x20] = [P(2, 6), P(6, 10), FONT_LAST]
fnt[ord("`") - 0x20] = [P(2, 10), P(6, 6), FONT_LAST]
fnt[ord("~") - 0x20] = [P(0, 4), P(2, 8), P(6, 4), P(8, 8), FONT_LAST]
fnt[ord("?") - 0x20] = [
    P(0, 8),
    P(4, 12),
    P(8, 8),
    P(4, 4),
    FONT_UP,
    P(4, 1),
    P(4, 0),
    FONT_LAST,
]
fnt[ord("A") - 0x20] = [
    P(0, 0),
    P(0, 8),
    P(4, 12),
    P(8, 8),
    P(8, 0),
    FONT_UP,
    P(0, 4),
    P(8, 4),
]
fnt[ord("B") - 0x20] = [
    P(0, 0),
    P(0, 12),
    P(4, 12),
    P(8, 10),
    P(4, 6),
    P(8, 2),
    P(4, 0),
    P(0, 0),
]
fnt[ord("C") - 0x20] = [P(8, 0), P(0, 0), P(0, 12), P(8, 12), FONT_LAST]
fnt[ord("D") - 0x20] = [
    P(0, 0),
    P(0, 12),
    P(4, 12),
    P(8, 8),
    P(8, 4),
    P(4, 0),
    P(0, 0),
    FONT_LAST,
]
fnt[ord("E") - 0x20] = [
    P(8, 0),
    P(0, 0),
    P(0, 12),
    P(8, 12),
    FONT_UP,
    P(0, 6),
    P(6, 6),
    FONT_LAST,
]
fnt[ord("F") - 0x20] = [
    P(0, 0),
    P(0, 12),
    P(8, 12),
    FONT_UP,
    P(0, 6),
    P(6, 6),
    FONT_LAST,
]
fnt[ord("G") - 0x20] = [
    P(6, 6),
    P(8, 4),
    P(8, 0),
    P(0, 0),
    P(0, 12),
    P(8, 12),
    FONT_LAST,
]
fnt[ord("H") - 0x20] = [
    P(0, 0),
    P(0, 12),
    FONT_UP,
    P(0, 6),
    P(8, 6),
    FONT_UP,
    P(8, 12),
    P(8, 0),
]
fnt[ord("I") - 0x20] = [
    P(0, 0),
    P(8, 0),
    FONT_UP,
    P(4, 0),
    P(4, 12),
    FONT_UP,
    P(0, 12),
    P(8, 12),
]
fnt[ord("J") - 0x20] = [P(0, 4), P(4, 0), P(8, 0), P(8, 12), FONT_LAST]
fnt[ord("K") - 0x20] = [
    P(0, 0),
    P(0, 12),
    FONT_UP,
    P(8, 12),
    P(0, 6),
    P(6, 0),
    FONT_LAST,
]
fnt[ord("L") - 0x20] = [P(8, 0), P(0, 0), P(0, 12), FONT_LAST]
fnt[ord("M") - 0x20] = [P(0, 0), P(0, 12), P(4, 8), P(8, 12), P(8, 0), FONT_LAST]
fnt[ord("N") - 0x20] = [P(0, 0), P(0, 12), P(8, 0), P(8, 12), FONT_LAST]
fnt[ord("O") - 0x20] = [P(0, 0), P(0, 12), P(8, 12), P(8, 0), P(0, 0), FONT_LAST]
fnt[ord("P") - 0x20] = [P(0, 0), P(0, 12), P(8, 12), P(8, 6), P(0, 5), FONT_LAST]
fnt[ord("Q") - 0x20] = [
    P(0, 0),
    P(0, 12),
    P(8, 12),
    P(8, 4),
    P(0, 0),
    FONT_UP,
    P(4, 4),
    P(8, 0),
]
fnt[ord("R") - 0x20] = [
    P(0, 0),
    P(0, 12),
    P(8, 12),
    P(8, 6),
    P(0, 5),
    FONT_UP,
    P(4, 5),
    P(8, 0),
]
fnt[ord("S") - 0x20] = [
    P(0, 2),
    P(2, 0),
    P(8, 0),
    P(8, 5),
    P(0, 7),
    P(0, 12),
    P(6, 12),
    P(8, 10),
]
fnt[ord("T") - 0x20] = [P(0, 12), P(8, 12), FONT_UP, P(4, 12), P(4, 0), FONT_LAST]
fnt[ord("U") - 0x20] = [P(0, 12), P(0, 2), P(4, 0), P(8, 2), P(8, 12), FONT_LAST]
fnt[ord("V") - 0x20] = [P(0, 12), P(4, 0), P(8, 12), FONT_LAST]
fnt[ord("W") - 0x20] = [P(0, 12), P(2, 0), P(4, 4), P(6, 0), P(8, 12), FONT_LAST]
fnt[ord("X") - 0x20] = [P(0, 0), P(8, 12), FONT_UP, P(0, 12), P(8, 0), FONT_LAST]
fnt[ord("Y") - 0x20] = [
    P(0, 12),
    P(4, 6),
    P(8, 12),
    FONT_UP,
    P(4, 6),
    P(4, 0),
    FONT_LAST,
]
fnt[ord("Z") - 0x20] = [
    P(0, 12),
    P(8, 12),
    P(0, 0),
    P(8, 0),
    FONT_UP,
    P(2, 6),
    P(6, 6),
    FONT_LAST,
]
