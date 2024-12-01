from board import Board
from structures import Player

board = Board(True, 4, Player.O)
board.initialize()
board.print()
print(board.halfPoints)
print(board.position_to_matrix('A1', 4))