from board import Board, draw_and_update, check_position, update_state, get_edges, position_to_matrix
from enums import Player, Direction
from copy import deepcopy

class Game:
    def __init__(self, isComputerPlaying: bool, boardSize: int, firstPlay: Player):
        self.board = Board(isComputerPlaying, boardSize, firstPlay)
        self.board.initialize()
        self.inputHistory = []

    def startGame(self):
        self.board.print()
        while not self.board.gameFinished:
            played = False
            while played is False:
                inpt = input(f'\n\nIgrac {self.board.currentPlayer.value} je na potezu: ')
                letter, number, direction = self.split_position(inpt)
                if inpt in self.inputHistory:
                    print(f'Potez {inpt} je vec odigran.')
                    break
                xPointsAdded, oPointsAdded, updateSuccessful = draw_and_update(self.board.board,self.board.boardSize ,self.board.branchState, self.board.triggleState, self.board.currentPlayer,letter, number, direction, True)
                self.board.xPoints += xPointsAdded
                self.board.oPoints += oPointsAdded
                if(updateSuccessful):
                    self.inputHistory.append(inpt)
                    played = True
                    print(f"Igrac {self.board.currentPlayer.name} je odigrao potez {letter}{number} {direction.name}.")
                    self.board.check_win()
                    self.board.print()
                    if self.board.currentPlayer == Player.X:
                        self.board.currentPlayer = Player.O
                    else:
                        self.board.currentPlayer = Player.X
                    print(f"Poeni igraca X: {self.board.xPoints}")
                    print(f"Poeni igraca O: {self.board.oPoints}")
        print("Igra je zavrsena. To ti je to baki.")
                    
                    
    def generate_all_moves(self):
        available_moves = []
        valid_letters = [chr(i) for i in range(ord('A'), ord('A') + 2*self.board.boardSize-1)]
        valid_numbers = range(1, 2*self.board.boardSize)
        valid_directions = list(Direction)
        
        for i in range(0, len(valid_letters)):
            for j in range(0, len(valid_numbers)):
                for k in range(0,3):
                    if check_position(self.board.board, self.board.boardSize, valid_letters[i], valid_numbers[j], valid_directions[k]):
                        position = f"{valid_letters[i]}{valid_numbers[j]} {valid_directions[k].value}"
                        if position not in self.inputHistory:
                            available_moves.append(position)
                            
        return available_moves
    
    def generate_all_states(self):
        all_moves = self.generate_all_moves()
        all_states = []
        current_branch_state = self.board.branchState
        current_triggle_state = self.board.triggleState
        current_player = self.board.currentPlayer
        
        for move in all_moves:
            letter, number, direction = self.split_position(move)
            row, col = position_to_matrix(self.board.boardSize, f"{letter}{number}")
            edges = get_edges(row,col, Direction(direction), self.board.boardSize)
            new_branch_state = deepcopy(current_branch_state)
            new_triggle_state = deepcopy(current_triggle_state)
            _, xPoints, oPoints = update_state(edges,new_branch_state,new_triggle_state,current_player)
            all_states.append((new_branch_state, new_triggle_state, xPoints, oPoints))
            
        return all_states
            
    def split_position(self, position):
        first, second = position.split()
        letter = first[0]
        number = int(first[1:])
        direction = Direction(second)
        return (letter, number, direction)