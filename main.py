from board import Board
from structures import Player, Direction

board = Board(True, 4, Player.O)
board.initialize()
board.draw_and_update(('A', 1, Direction.DL))
board.draw_and_update(('A', 1, Direction.DD))
board.draw_and_update(('B', 1, Direction.D))
board.print()