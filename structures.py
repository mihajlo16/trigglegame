from enum import Enum

class Player(Enum):
    N = ""
    X = "X"
    O = "O"

class Direction(Enum):
    D = "Desno"
    DD = "DoleDesno"
    DL = "DoleLevo"