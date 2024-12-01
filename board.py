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
        self.initializeState()

    # Stampanje table u konzoli
    def print(self):
        for row in self.board:
            print(row)

    # Provera da li je igra gotova
    def check_win(self):
        if self.oPoints > self.halfPoints:
            print(f"Pobedio je igrac {Player.O}!")
            self.gameFinished = True
        elif self.xPoints > self.halfPoints:
            print(f"Pobedio je igrac {Player.X}!")
            self.gameFinished = True
        elif self.oPoints == self.halfPoints and self.xPoints == self.halfPoints:
            print("Rezultat je neresen!")
            self.gameFinished = True

    # Prevod pozicije na tabli u indeks matrice
    def position_to_matrix(self, position):
        letter = position[0]
        number = int(position[1:])

        actual_row = ord(letter.upper()) - 65

        row = actual_row * 3
        if actual_row == self.boardSize - 1:
            col = 2 + 6 * (number - 1)
        elif actual_row < self.boardSize - 1:
            col = 3 * (abs(self.boardSize - 1 - actual_row)) + 2 + 6 * (number - 1)
        else:
            col = 3 * (abs(-self.boardSize + 1 + actual_row)) + 2 + 6 * (number - 1)
        return row, col
    

    # Prevod indeksa matrice u poziciju na tabli
    def matrix_to_position(self, row, col):
        actual_row = row // 3
        letter = chr(65 + actual_row)

        if actual_row == self.boardSize - 1:
            number = (col - 2) // 6 + 1
        elif actual_row < self.boardSize - 1:
            offset = 3 * (self.boardSize - 1 - actual_row)
            number = (col - offset - 2) // 6 + 1
        else:
            offset = 3 * (actual_row - (self.boardSize - 1))
            number = (col - offset - 2) // 6 + 1

        return f"{letter}{number}"
    

    # Postavka inicijalnog stanja
    def initializeState(self):
        vertex_positions = {}

        for row in range(0, len(self.board), 3):
            for col in range(2, len(self.board[row]), 1):
                if self.board[row][col] == "*":
                    vertex_label = self.matrix_to_position(row, col)
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
                neighbor_label = self.matrix_to_position(neighbor_row, neighbor_col)
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
                self.matrix_to_position(row + 3, col),
                self.matrix_to_position(row, col + 6),
                self.matrix_to_position(row + 3, col + 6)
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



    def check_position(self, letter:str, number: int, direction: Direction):
        if (
        not isinstance(letter, str) or len(letter) != 1 or not letter.isupper() or
        not isinstance(number, int) or number < 1 or
        not isinstance(direction, Direction)):
            print(f"Neispravni parametri pozicije: {letter}{number} {direction}")
            return False

        valid_letters = [chr(i) for i in range(ord('A'), ord('A') + 2*self.boardSize-1)]
        valid_numbers = range(1, 2*self.boardSize)
        letter_index = ord(letter) - ord('A')
        
        if letter not in valid_letters:
            print(f"Neispravno slovo: {letter}. Dozvoljeno: {valid_letters}.")
            return False

        if number not in valid_numbers:
            print(f"Neispravan broj: {number}. Dozvoljeno: {list(valid_numbers)}.")
            return False
        
        if direction == Direction.D:
            if letter_index < self.boardSize and letter_index + 1 < number:
                print(f"Ne smete koristiti D za poziciju {letter}{number}.")
                return False
            elif letter_index >= self.boardSize and -(letter_index - 2*self.boardSize + 2) + 1 < number:
                print(f"Ne smete koristiti D za poziciju {letter}{number}.")
                return False

        if direction == Direction.DD:
            if not (letter_index < 2 * self.boardSize - 1 - 3 and number <= self.boardSize):
                print(f"Ne smete koristiti DD za poziciju {letter}{number}.")
                return False

        if direction == Direction.DL:
            if not (letter_index < 2 * self.boardSize - 1 - 3 and number >= letter_index + 1):
                print(f"Ne smete koristiti DL za poziciju {letter}{number}.")
                return False
        
        return True

            
    
    # Postavka gumice na odredjenu poziciju
    # Vraca True ukoliko je potez uspesno odigran
    def draw_and_update(self, letter:str, number: int, direction: Direction):
        if(self.gameFinished):
            print("Igra je zavrsena. Ne mozete odigrati potez.")
            return False

        if(not(self.check_position(letter, number, direction))):
            return False

        row, col = self.position_to_matrix(f"{letter}{number}")

        if direction == Direction.D:
            edges = [
                (self.matrix_to_position(row, col), self.matrix_to_position(row, col + 6)),
                (self.matrix_to_position(row, col + 6), self.matrix_to_position(row, col + 12)),
                (self.matrix_to_position(row, col + 12), self.matrix_to_position(row, col + 18)),
            ]
            char = "-"
        elif direction == Direction.DL:
            edges = [
                (self.matrix_to_position(row, col), self.matrix_to_position(row + 3, col - 3)),
                (self.matrix_to_position(row + 3, col - 3), self.matrix_to_position(row + 6, col - 6)),
                (self.matrix_to_position(row + 6, col - 6), self.matrix_to_position(row + 9, col - 9)),
            ]
            char = "/"
        elif direction == Direction.DD:
            edges = [
                (self.matrix_to_position(row, col), self.matrix_to_position(row + 3, col + 3)),
                (self.matrix_to_position(row + 3, col + 3), self.matrix_to_position(row + 6, col + 6)),
                (self.matrix_to_position(row + 6, col + 6), self.matrix_to_position(row + 9, col + 9)),
            ]
            char = "\\"
        else:
            raise ValueError("Neispravan smer! Dozvoljeni smerovi su 'D', 'DL', 'DD'.")
        
        edge_ids=[]
        for edge in edges:
            edge_id = None
            for branch_id, branch_data in self.branchState.items():
                if set(branch_data['edge']) == set(edge):
                    edge_id = branch_id
                    break
            if edge_id is not None:
                self.branchState[edge_id]['isOccupied'] = True
                edge_ids.append(edge_id)
            else:
                raise ValueError(f"Grana {edge} nije pronadjena!")
                        

            if char == "-":
                self.board[row] = (
                    self.board[row][:col + 1]
                    + 5 * "-"
                    + self.board[row][col + 6:]
                )
                col = col + 6
            elif char == "\\":
                self.board[row + 1] = (
                    self.board[row + 1][:col+1]
                    + "\\"
                    + self.board[row + 1][col + 2:]
                )
                self.board[row + 2] = (
                    self.board[row + 2][:col + 2]
                    + "\\"
                    + self.board[row + 2][col + 3:]
                )
                col = col + 3
                row = row + 3

            elif char == "/":
                self.board[row + 1] = (
                    self.board[row + 1][:col-1]
                    + "/"
                    + self.board[row + 1][col:]
                )
                self.board[row + 2] = (
                    self.board[row + 2][:col - 2]
                    + "/"
                    + self.board[row + 2][col - 1:]
                )
                col = col - 3
                row = row + 3

        for triangle_key, triangle_data in self.triggleState.items():            
            grane_trougla = [self.branchState[branch_id]['isOccupied'] for branch_id in triangle_key]
            
            if all(grane_trougla):

                if triangle_data["igracKojiJeZauzeo"] == Player.N:
                    triangle_data["igracKojiJeZauzeo"] = self.currentPlayer
                    if(self.currentPlayer==Player.O):
                        self.oPoints=self.oPoints+1
                    else:
                        self.xPoints+=1
                    center_row, center_col = triangle_data["indeksUMatrici"]

                    self.board[center_row] = (
                        self.board[center_row][:center_col]
                        + self.currentPlayer.value
                        + self.board[center_row][center_col + 1:]
                    )

        return True





