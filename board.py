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


    def matrix_to_position(self, row, col, board_size):
        if row % 3 != 0:
            raise ValueError("Pozicija mora biti na liniji sa stubićima.")

        actual_row = row // 3  # Računamo stvarni red
        if actual_row < board_size:  # Gornji deo i srednji red
            start_offset = (board_size - actual_row - 1) * 3
            max_in_row = board_size + actual_row
        else:  # Donji deo
            adjusted_row = actual_row - board_size + 1
            start_offset = (adjusted_row + 1) * 3
            max_in_row = board_size + (board_size - adjusted_row - 2)

    # Proveravamo validnost kolone
        actual_col = (col - start_offset) // 6
        if actual_col < 0 or actual_col >= max_in_row:
            raise ValueError("Kolona je van opsega za dati red.")

        return f"{chr(65 + actual_row)}{actual_col + 1}"


    def position_to_matrix(self, position, board_size):
        letter = position[0]
        number = int(position[1:]) - 1

        actual_row = ord(letter.upper()) - 65
        if actual_row < board_size:  # Gornji deo i srednji red
            start_offset = (board_size - actual_row - 1) * 3
            max_in_row = board_size + actual_row
        else:  # Donji deo
            adjusted_row = actual_row - board_size + 1
            start_offset = (adjusted_row + 1) * 3
            max_in_row = board_size + (board_size - adjusted_row - 2)

        if number < 0 or number >= max_in_row:
            raise ValueError("Pozicija je van opsega za dati red.")

        row = actual_row * 3
        col = start_offset + number * 6
        return row, col


