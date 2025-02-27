from board import Board, draw_and_update, check_position
from enums import Player, Direction
from copy import deepcopy

class Game:
    def __init__(self, isComputerPlaying: bool, boardSize: int, firstPlay: Player):
        self.board = Board(isComputerPlaying, boardSize, firstPlay)
        self.board.initialize()
        self.inputHistory = []

    def startGame(self, depth):
        self.board.print()
        while not self.board.gameFinished:
            played = False
            while played is False:
                if self.board.isComputerPlaying and self.board.currentPlayer == Player.X:
                    print("\nRačunar je na potezu...")
                    best_move = self.get_best_move(depth)
                    print(f"Računar bira potez: {best_move}")
                else:
                    best_move = input(f'\n\nIgrac {self.board.currentPlayer.value} je na potezu: ')
                
                letter, number, direction = self.split_position(best_move)
                if best_move in self.inputHistory:
                    print(f'Potez {best_move} je već odigran.')
                    continue
                
                updateSuccessful = draw_and_update(
                    self.board.board, self.board.boardSize, self.board.branchState,
                    self.board.triggleState, self.board.currentPlayer, letter, number, direction, True
                )

                if not updateSuccessful:
                    continue

                self.inputHistory.append(best_move)
                played = True
                print(f"Igrac {self.board.currentPlayer.name} je odigrao potez {letter}{number} {direction.name}.")
                self.board.check_win()
                self.board.print()
                self.board.currentPlayer = Player.O if self.board.currentPlayer == Player.X else Player.X
                print(f"Poeni igraca X: {self.board.xPoints}")
                print(f"Poeni igraca O: {self.board.oPoints}")
        
        print("Igra je završena.")

    def get_best_move(self, depth):
        best_move = None
        best_value = float('-inf')
        alpha, beta = float('-inf'), float('inf')

        for move in self.generate_all_moves():  # FIX: Pozivamo iz Game klase, ne Board
            letter, number, direction = self.split_position(move)

            if not check_position(self.board.board, self.board.boardSize, letter, number, direction, False):
                continue

            new_board = deepcopy(self.board)
            new_branchState = deepcopy(self.board.branchState)
            new_triggleState = deepcopy(self.board.triggleState)

            updateSuccessful = draw_and_update(
                new_board.board, new_board.boardSize, new_branchState,
                new_triggleState, new_board.currentPlayer, letter, number, direction, printMsg=False
            )

            if not updateSuccessful:
                continue

            new_board.currentPlayer = Player.O if new_board.currentPlayer == Player.X else Player.X

            move_value = self.minimax(new_board, new_branchState, new_triggleState, depth-1, alpha, beta, False)

            if move_value > best_value:
                best_value = move_value
                best_move = move

            alpha = max(alpha, best_value)
            if beta <= alpha:
                break  # α-β odsecanje

        return best_move

    def split_position(self, position):
        first, second = position.split()
        letter = first[0]
        number = int(first[1:])
        direction = Direction(second)
        return (letter, number, direction)

    def generate_all_moves(self):
        available_moves = []
        valid_letters = [chr(i) for i in range(ord('A'), ord('A') + 2*self.board.boardSize-1)]
        valid_numbers = range(1, 2*self.board.boardSize)
        valid_directions = list(Direction)

        for i in range(len(valid_letters)):
            for j in range(len(valid_numbers)):
                for k in range(3):
                    if check_position(self.board.board, self.board.boardSize, valid_letters[i], valid_numbers[j], valid_directions[k], False):
                        position = f"{valid_letters[i]}{valid_numbers[j]} {valid_directions[k].value}"
                        if position not in self.inputHistory:
                            available_moves.append(position)

        return available_moves

    def minimax(self, board, branchState, triggleState, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or board.gameFinished:
            return self.heuristic(board, board.currentPlayer)

        if maximizingPlayer:
            maxEval = float('-inf')
            for move in self.generate_all_moves():  # FIX: Poziv iz Game klase, ne Board
                letter, number, direction = self.split_position(move)

                if not check_position(board.board, board.boardSize, letter, number, direction, False):
                    continue

                new_board = deepcopy(board)
                new_branchState = deepcopy(branchState)
                new_triggleState = deepcopy(triggleState)

                updateSuccessful = draw_and_update(
                    new_board.board, new_board.boardSize, new_branchState,
                    new_triggleState, new_board.currentPlayer, letter, number, direction, printMsg=False
                )

                if not updateSuccessful:
                    continue  

                new_board.currentPlayer = Player.O if new_board.currentPlayer == Player.X else Player.X

                eval = self.minimax(new_board, new_branchState, new_triggleState, depth-1, alpha, beta, False)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  
            return maxEval
        else:
            minEval = float('inf')
            for move in self.generate_all_moves():  # FIX: Poziv iz Game klase, ne Board
                letter, number, direction = self.split_position(move)

                if not check_position(board.board, board.boardSize, letter, number, direction, False):
                    continue

                new_board = deepcopy(board)
                new_branchState = deepcopy(branchState)
                new_triggleState = deepcopy(triggleState)

                updateSuccessful = draw_and_update(
                    new_board.board, new_board.boardSize, new_branchState,
                    new_triggleState, new_board.currentPlayer, letter, number, direction, printMsg=False
                )

                if not updateSuccessful:
                    continue  

                new_board.currentPlayer = Player.O if new_board.currentPlayer == Player.X else Player.X

                eval = self.minimax(new_board, new_branchState, new_triggleState, depth-1, alpha, beta, True)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval

    def heuristic(self, board, player):
        score = 0
        for triangle in board.triggleState.values():
            if triangle["igracKojiJeZauzeo"] == player:
                score += 1  
            elif triangle["igracKojiJeZauzeo"] == Player.N:
                score += 0.5  
        return score