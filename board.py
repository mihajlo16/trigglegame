from enums import Player, Direction
from itertools import combinations

class Board:
    def __init__(self, isComputerPlaying: bool, boardSize: int, firstPlay: Player):
        if(boardSize < 4 or boardSize > 8):
            raise ValueError("Velicina table mora biti izmedju 4 i 8.")

        self.isComputerPlaying = isComputerPlaying
        self.boardSize = boardSize
        self.currentPlayer = firstPlay
        self.oPoints = 0
        self.xPoints = 0
        self.halfPoints = (6 * ((boardSize - 1) ** 2)) // 2
        self.board = []
        self.branchState = {}
        self.triggleState = {}
        self.gameFinished = False

    @property
    def currentPlayer(self):
        return self._currentPlayer

    @currentPlayer.setter
    def currentPlayer(self, value: Player):
        if not isinstance(value, Player):
            raise ValueError("Nevalidan igrac. Mora biti instanca Player.")
        self._currentPlayer = value


    # Inicijalna priprema table
    def initialize(self):
        self.gameFinished = False
        space = "   "
        star = "  *   "
        max_width = 2 * (2 * self.boardSize - 1)
    
        temp_board = []
        
        for i in range(self.boardSize):
            spaces = space * (self.boardSize - i - 1)
            stars = star * (self.boardSize + i)
            temp_board.append(spaces + stars)
            temp_board.append(space * max_width)
            temp_board.append(space * max_width)

        for i in range(self.boardSize - 2, -1, -1):
            spaces = space * (self.boardSize - i - 1)
            stars = star * (self.boardSize + i)
            temp_board.append(spaces + stars)
            temp_board.append(space * max_width)
            temp_board.append(space * max_width)
        
        max_row_length = max(len(row) for row in temp_board)
        
        self.board = [row.ljust(max_row_length, ' ') for row in temp_board]
        self.initializeState()

    # Stampanje table u konzoli
    def print(self):
        for row in self.board:
            print(row)

    # Provera da li je igra gotova
    def check_win(self):
        if self.oPoints > self.halfPoints:
            print(f"Pobedio je igrac {Player.O.name}!")
            self.gameFinished = True
        elif self.xPoints > self.halfPoints:
            print(f"Pobedio je igrac {Player.X.name}!")
            self.gameFinished = True
        elif self.oPoints == self.halfPoints and self.xPoints == self.halfPoints:
            print("Rezultat je neresen!")
            self.gameFinished = True
    

    # Postavka inicijalnog stanja
    def initializeState(self):
        vertex_positions = {}

        for row in range(0, len(self.board), 3):
            for col in range(2, len(self.board[row]), 1):
                if self.board[row][col] == "*":
                    vertex_label = matrix_to_position(self.boardSize, row, col)
                    vertex_positions[vertex_label] = (row, col)

        self.branchState = {}
        branch_id_map = {}
        branch_counter = 0

        for vertex, (row, col) in vertex_positions.items():
            neighbors = [
                (row + 3, col),
                (row, col + 6),
                (row + 3, col + 6),
            ]

            for neighbor_row, neighbor_col in neighbors:
                neighbor_label = matrix_to_position(self.boardSize, neighbor_row, neighbor_col)
                if neighbor_label in vertex_positions:
                    edge = tuple(sorted([vertex, neighbor_label]))
                    if edge not in branch_id_map:
                        branch_id_map[edge] = branch_counter
                        self.branchState[branch_counter] = {
                            'edge': edge,
                            'isOccupied': False
                        }
                        branch_counter += 1

        self.triggleState = {}
        for vertex, (row, col) in vertex_positions.items():
            neighbors = [
                matrix_to_position(self.boardSize, row + 3, col),
                matrix_to_position(self.boardSize, row, col + 6),
                matrix_to_position(self.boardSize, row + 3, col + 6)
            ]
            valid_neighbors = [n for n in neighbors if n in vertex_positions]

            for n1, n2 in combinations(valid_neighbors, 2):
                triangle_edges = [
                    tuple(sorted([vertex, n1])),
                    tuple(sorted([vertex, n2])),
                    tuple(sorted([n1, n2]))
                ]
                if all(edge in branch_id_map for edge in triangle_edges):
                    edge_ids = tuple(sorted(branch_id_map[edge] for edge in triangle_edges))

                    triangle_vertices = [
                        vertex_positions[vertex],
                        vertex_positions[n1],
                        vertex_positions[n2]
                    ]
                    center_row = sum(v[0] for v in triangle_vertices) // 3
                    center_col = sum(v[1] for v in triangle_vertices) // 3

                    if edge_ids not in self.triggleState:
                        self.triggleState[edge_ids] = {
                            "igracKojiJeZauzeo": Player.N,
                            "indeksUMatrici": (center_row, center_col)
                        }



def check_position(board, boardSize, letter:str, number: int, direction: Direction, printMsg: bool):
    if (
        not isinstance(letter, str) or len(letter) != 1 or not letter.isupper() or
        not isinstance(number, int) or number < 1 or
        not isinstance(direction, Direction)):
        if printMsg: print(f"Neispravni parametri pozicije: {letter}{number} {direction}")
        return False
    
    valid_numbers = get_valid_numbers(boardSize, letter)
    valid_letters = [chr(i) for i in range(ord('A'), ord('A') + 2*boardSize-1)]
    
    if letter not in valid_letters:
        if printMsg: print(f"Neispravno slovo: {letter}. Dozvoljeno: {valid_letters}.")
        return False

    if number not in valid_numbers:
        if printMsg: print(f"Neispravan broj: {number}. Dozvoljeno: {list(valid_numbers)}.")
        return False

    realBoardHeight = len(board)
    realBoardWidth = max(len(row) for row in board)
    
    row, col = position_to_matrix(boardSize, f"{letter}{number}")

    if direction == Direction.D:
        if col + 18 >= realBoardWidth:
            if printMsg: print(f"Ne smete koristiti D za poziciju {letter}{number}.")
            return False
        if board[row][col+18] != '*':
            if printMsg: print(f"Ne smete koristiti D za poziciju {letter}{number}.")
            return False

    if direction == Direction.DD:
        if col + 9 >= realBoardWidth or row + 9 >= realBoardHeight:
            if printMsg: print(f"Ne smete koristiti DD za poziciju {letter}{number}.")
            return False
        if board[row+9][col+9] != '*':
            if printMsg: print(f"Ne smete koristiti D za poziciju {letter}{number}.")
            return False

    if direction == Direction.DL:
        if col - 9 < 0 or col - 9 >= realBoardWidth or row + 9 >= realBoardHeight:
            if printMsg: print(f"Ne smete koristiti DL za poziciju {letter}{number}.")
            return False
        if board[row+9][col-9] != '*':
            if printMsg: print(f"Ne smete koristiti D za poziciju {letter}{number}.")
            return False
    
    return True
    
# Postavka gumice na odredjenu poziciju
# Vraca True ukoliko je potez uspesno odigran
def draw_and_update(board: list, boardSize: int, branch_state: dict, triggle_state: dict, current_player: Player, letter: str, number: int, direction: Direction, printMsg: bool):
    if not check_position(board, boardSize,letter, number, direction, printMsg):
        return (0, 0, False)

    row, col = position_to_matrix(boardSize, f"{letter}{number}")
    edges, char = get_edges(row, col, direction, boardSize)
    
    for _ in range(0, len(edges)):
        if char == "-":
            board[row] = (
                board[row][:col + 1]
                + 5 * "-"
                + board[row][col + 6:]
            )
            col = col + 6
        elif char == "\\":
            board[row + 1] = (
                board[row + 1][:col+1]
                + "\\"
                + board[row + 1][col + 2:]
            )
            board[row + 2] = (
                board[row + 2][:col + 2]
                + "\\"
                + board[row + 2][col + 3:]
            )
            col = col + 3
            row = row + 3

        elif char == "/":
            board[row + 1] = (
                board[row + 1][:col-1]
                + "/"
                + board[row + 1][col:]
            )
            board[row + 2] = (
                board[row + 2][:col - 2]
                + "/"
                + board[row + 2][col - 1:]
            )
            col = col - 3
            row = row + 3
            
    triangle_data, xPoints, oPoints = update_state(edges, branch_state, triggle_state, current_player)
            
    center_row, center_col = triangle_data
    
    if center_row is not -1 and center_col is not -1:
        board[center_row] = (
            board[center_row][:center_col]
            + current_player.value
            + board[center_row][center_col + 1:]
        )

    return (xPoints, oPoints, True)


def update_state(edges: list, branch_state: dict, triggle_state: dict, current_player: Player):
    xPoints = 0
    oPoints = 0
    
    edge_ids = []
    for edge in edges:
        edge_id = None
        for branch_id, branch_data in branch_state.items():
            if set(branch_data['edge']) == set(edge):
                edge_id = branch_id
                break
        if edge_id is not None:
            branch_state[edge_id]['isOccupied'] = True
            edge_ids.append(edge_id)
        else:
            print(f"Grana {edge} nije pronadjena!")
            return (xPoints, oPoints, False)
        
    for triangle_key, triangle_data in triggle_state.items():            
        grane_trougla = [branch_state[branch_id]['isOccupied'] for branch_id in triangle_key]
        
        if all(grane_trougla):

                if triangle_data["igracKojiJeZauzeo"] == Player.N:
                    triangle_data["igracKojiJeZauzeo"] = current_player
                    if(current_player==Player.O):
                        oPoints+=1
                    else:
                        xPoints+=1
                    return (triangle_data["indeksUMatrici"], xPoints, oPoints)
    
    return ((-1,-1), xPoints, oPoints)


# Prevod pozicije na tabli u indeks matrice
def position_to_matrix(boardSize, position):
    letter = position[0]
    number = int(position[1:])

    actual_row = ord(letter.upper()) - 65

    row = actual_row * 3
    if actual_row == boardSize - 1:
        col = 2 + 6 * (number - 1)
    elif actual_row < boardSize - 1:
        col = 3 * (abs(boardSize - 1 - actual_row)) + 2 + 6 * (number - 1)
    else:
        col = 3 * (abs(-boardSize + 1 + actual_row)) + 2 + 6 * (number - 1)
    return row, col


# Prevod indeksa matrice u poziciju na tabli
def matrix_to_position(boardSize, row, col):
    actual_row = row // 3
    letter = chr(65 + actual_row)

    if actual_row == boardSize - 1:
        number = (col - 2) // 6 + 1
    elif actual_row < boardSize - 1:
        offset = 3 * (boardSize - 1 - actual_row)
        number = (col - offset - 2) // 6 + 1
    else:
        offset = 3 * (actual_row - (boardSize - 1))
        number = (col - offset - 2) // 6 + 1

    return f"{letter}{number}"

def letter_to_number(letter):
    return ord(letter.upper()) - ord('A') + 1

def get_valid_numbers(boardSize, letter):
    valid_numbers = []
    number_of_letter = letter_to_number(letter)
    
    if(number_of_letter <= boardSize):
        valid_numbers = range(1, boardSize + number_of_letter)
    else:
        valid_numbers = range(1, 2 * boardSize - (number_of_letter % boardSize))
    return valid_numbers

def get_edges(row, col, direction, boardSize):
    char = ""
    edges = []
    if direction == Direction.D:
        edges = [
            (matrix_to_position(boardSize,row, col), matrix_to_position(boardSize,row, col + 6)),
            (matrix_to_position(boardSize,row, col + 6), matrix_to_position(boardSize,row, col + 12)),
            (matrix_to_position(boardSize,row, col + 12), matrix_to_position(boardSize,row, col + 18)),
        ]
        char = "-"
    elif direction == Direction.DL:
        edges = [
            (matrix_to_position(boardSize,row, col), matrix_to_position(boardSize,row + 3, col - 3)),
            (matrix_to_position(boardSize,row + 3, col - 3), matrix_to_position(boardSize,row + 6, col - 6)),
            (matrix_to_position(boardSize,row + 6, col - 6), matrix_to_position(boardSize,row + 9, col - 9)),
        ]
        char = "/"
    elif direction == Direction.DD:
        edges = [
            (matrix_to_position(boardSize,row, col), matrix_to_position(boardSize,row + 3, col + 3)),
            (matrix_to_position(boardSize,row + 3, col + 3), matrix_to_position(boardSize,row + 6, col + 6)),
            (matrix_to_position(boardSize,row + 6, col + 6), matrix_to_position(boardSize,row + 9, col + 9)),
        ]
        char = "\\"
        
    return (edges, char)