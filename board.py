from structures import Player, Direction
from itertools import combinations

class Board:
    def __init__(self, isComputerPlaying, boardSize, firstPlay: Player):
        self.isComputerPlaying = isComputerPlaying
        self.boardSize = boardSize
        self.currentPlayer = firstPlay
        self.oPoints = 0
        self.xPoints = 0
        self.halfPoints = (6 * ((boardSize - 1) ** 2)) // 2
        self.board = []
        self.branchState = {}
        self.triggleState = {}

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
        self.initializeState()

    def print(self):
        for row in self.board:
            print(row)

    def check_win(self):
        if self.oPoints > self.halfPoints:
            print(f"Pobedio je igrac {Player.O}!")
        elif self.xPoints > self.halfPoints:
            print(f"Pobedio je igrac {Player.X}!")
        elif self.oPoints == self.halfPoints and self.xPoints == self.halfPoints:
            print("Rezultat je neresen!")

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


    def initializeState(self):
        vertex_positions = {}

        # Identifikuj temena i njihove pozicije
        for row in range(0, len(self.board), 3):
            for col in range(2, len(self.board[row]), 1):
                if self.board[row][col] == "*":
                    vertex_label = self.matrix_to_position(row, col)
                    vertex_positions[vertex_label] = (row, col)

        # Generisanje grana sa ID-ovima
        self.branchState = {}
        branch_id_map = {}
        branch_counter = 0

        for vertex, (row, col) in vertex_positions.items():
            neighbors = [
                (row + 3, col),       # Donji centar
                (row, col + 6),       # Desno
                (row + 3, col + 6),   # Donji-desno
            ]

            # Proveri validne susede i kreiraj grane
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

        # Generisanje trouglova sa ID-ovima grana
        self.triggleState = {}
        for vertex, (row, col) in vertex_positions.items():
            # Pronađi susede za trenutni vertex
            neighbors = [
                self.matrix_to_position(row + 3, col),       # Donji centar
                self.matrix_to_position(row, col + 6),       # Desno
                self.matrix_to_position(row + 3, col + 6)    # Donji-desno
            ]
            valid_neighbors = [n for n in neighbors if n in vertex_positions]

            # Formiraj trouglove sa trenutnim temenom
            for n1, n2 in combinations(valid_neighbors, 2):
                triangle_edges = [
                    tuple(sorted([vertex, n1])),
                    tuple(sorted([vertex, n2])),
                    tuple(sorted([n1, n2]))
                ]
                # Proveri da li sve grane trougla postoje
                if all(edge in branch_id_map for edge in triangle_edges):
                    # Mapiraj grane na ID-ove
                    edge_ids = tuple(sorted(branch_id_map[edge] for edge in triangle_edges))

                    # Izračunaj središte trougla
                    triangle_vertices = [
                        vertex_positions[vertex],
                        vertex_positions[n1],
                        vertex_positions[n2]
                    ]
                    center_row = sum(v[0] for v in triangle_vertices) // 3
                    center_col = sum(v[1] for v in triangle_vertices) // 3

                    # Dodaj trougao u triggleState
                    if edge_ids not in self.triggleState:
                        self.triggleState[edge_ids] = {
                            "igracKojiJeZauzeo": Player.N,
                            "indeksUMatrici": (center_row, center_col)
                        }


    def draw_and_update(self, position: tuple):
        """
        Crta gumice, postavlja stanje za grane i ažurira zauzete trouglove.

        :param position: Tuple u formatu ('B', 1, 'DD'), gde:
            - 'B' je red označen slovom
            - 1 je broj kolone
            - 'D', 'DL', 'DD' su pravci (desno, dole-levo, dole-desno)
        """
        letter, number, direction = position
        row, col = self.position_to_matrix(f"{letter}{number}")

        # Definiši grane koje treba da se zauzmu na osnovu smera
        # Definiši grane koje treba da se zauzmu na osnovu smera
        if direction == Direction.D:  # Desno
            edges = [
                (self.matrix_to_position(row, col), self.matrix_to_position(row, col + 6)),  # Prva grana
                (self.matrix_to_position(row, col + 6), self.matrix_to_position(row, col + 12)),  # Druga grana
                (self.matrix_to_position(row, col + 12), self.matrix_to_position(row, col + 18)),  # Treća grana
            ]
            char = "-"
        elif direction == Direction.DL:  # Dole-levo
            edges = [
                (self.matrix_to_position(row, col), self.matrix_to_position(row + 3, col - 3)),  # Prva grana
                (self.matrix_to_position(row + 3, col - 3), self.matrix_to_position(row + 6, col - 6)),  # Druga grana
                (self.matrix_to_position(row + 6, col - 6), self.matrix_to_position(row + 9, col - 9)),  # Treća grana
            ]
            char = "/"
        elif direction == Direction.DD:  # Dole-desno
            edges = [
                (self.matrix_to_position(row, col), self.matrix_to_position(row + 3, col + 3)),  # Prva grana
                (self.matrix_to_position(row + 3, col + 3), self.matrix_to_position(row + 6, col + 6)),  # Druga grana
                (self.matrix_to_position(row + 6, col + 6), self.matrix_to_position(row + 9, col + 9)),  # Treća grana
            ]
            char = "\\"
        else:
            raise ValueError("Neispravan smer! Dozvoljeni smerovi su 'D', 'DL', 'DD'.")
        

        # Postavi grane na zauzeto i nacrtaj na tabli
        for edge in edges:
            # Pronađi ID grane i postavi stanje na zauzeto
            edge_id = None
            for branch_id, branch_data in self.branchState.items():
                if set(branch_data['edge']) == set(edge):
                    edge_id = branch_id
                    break
            if edge_id is not None:
                self.branchState[edge_id]['isOccupied'] = True
            else:
                raise ValueError(f"Grana {edge} nije pronađena!")
            
            

            if char == "-":  # Desno
                self.board[row] = (
                    self.board[row][:col + 1]
                    + 5 * "-"
                    + self.board[row][col + 6:]
                )
                col = col + 6
            elif char == "\\":  # Dole-desno
                self.board[row + 1] = (
                    self.board[row + 1][:col + 1]
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

            elif char == "/":  # Dole-levo
                self.board[row + 1] = (
                    self.board[row + 1][:col - 1]
                    + "/"
                    + self.board[row + 1][col - 2:]
                )
                self.board[row + 2] = (
                    self.board[row + 2][:col - 2]
                    + "/"
                    + self.board[row + 2][col - 3:]
                )
                col = col - 3
                row = row + 3

        # Proveri da li su trouglovi zauzeti i ažuriraj
        # Proveri da li su trouglovi zauzeti i ažuriraj
        print(edge_id)
        for triangle_key, triangle_data in self.triggleState.items():
            print(f"Proveravam trougao: {triangle_key}")
            if edge_id in triangle_key:  # Proveri da li edge_id pripada trouglu
                # Proveri da li su sve grane trougla zauzete
                if all(self.branchState[branch_id]['isOccupied'] for branch_id in triangle_key):
                    # Postavi zauzeće trougla
                    if triangle_data["igracKojiJeZauzeo"] == Player.N:
                        print(f"Trougao zauzet: {triangle_key}")
                        triangle_data["igracKojiJeZauzeo"] = self.currentPlayer
                        center_row, center_col = triangle_data["indeksUMatrici"]

                        # Nacrtaj trougao
                        self.board[center_row] = (
                            self.board[center_row][:center_col]
                            + self.currentPlayer.value
                            + self.board[center_row][center_col + 1:]
                        )


