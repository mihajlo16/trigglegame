from structures import Player

class Board:
    def __init__(self, isComputerPlaying, boardSize, firstPlay: Player):
        self.isComputerPlaying = isComputerPlaying
        self.boardSize = boardSize
        self.currentPlayer = firstPlay
        self.oPoints = 0
        self.xPoints = 0
        self.halfPoints = (6 * ((boardSize - 1) ** 2)) // 2
        self.board = []

    def initialize(self):
        space = "   "
        star = "  *   "
        max_width = 2 * (2 * self.boardSize - 1) 
        for i in range(self.boardSize):
            spaces = space * (self.boardSize - i - 1)
            stars = star * (self.boardSize + i)
            self.board.append(spaces + stars)
            self.board.append(space * max_width)
            self.board.append(space * max_width)

        for i in range(self.boardSize - 2, -1, -1):
            spaces = space * (self.boardSize - i - 1)
            stars = star * (self.boardSize + i)
            self.board.append(spaces + stars)
            self.board.append(space * max_width)
            self.board.append(space * max_width)


    def print(self):
        for row in self.board:
            print(row)


    def check_win(self):
        if(self.oPoints > self.halfPoints):
            print(f"Pobedio je igrac {Player.O}!")
        if(self.xPoints > self.halfPoints):
            print(f"Pobedio je igrac {Player.X}!")
        if(self.oPoints == self.halfPoints and self.xPoints == self.halfPoints):
            print("Rezultat je neresen!")


    def position_to_matrix(self, position):
        letter = position[0]
        number = int(position[1:])

        actual_row = ord(letter.upper()) - 65

        row = actual_row * 3
        if(actual_row == self.boardSize - 1):
            col = 2 + 6 * (number - 1)
        if(actual_row < self.boardSize - 1):
            col = 3 * (abs(self.boardSize - 1 - actual_row)) + 2 + 6 * (number - 1)
        else:
            col = 3 * (abs(-self.boardSize + 1 + actual_row)) + 2 + 6 * (number - 1)
        return row, col


