from board import Board
from structures import Player, Direction

board = Board(True, 4, Player.O)
board.initialize()
try:
    # board.draw_and_update(('A', 1, Direction.DL))
    # board.draw_and_update(('A', 1, Direction.DD))
    # board.draw_and_update(('B', 1, Direction.D))
    # board.draw_and_update(('B', 1, Direction.DD))
    # board.draw_and_update(('C', 1, Direction.D))
    # board.draw_and_update(('A', 2, Direction.DL))
    # board.draw_and_update(('A', 3, Direction.DL))
    board.draw_and_update(('D', 4, Direction.D))
except Exception as e:
    print(f"Greška: {e}")
print(board.oPoints)
board.print()