from enums import Player, Direction
from board import Board

def testRound(board: Board, position: tuple):
    board.draw_and_update(position)
    print(f"Igrac {board.currentPlayer} je odigrao potez {position}")
    board.check_win()
    if board.currentPlayer == Player.X:
        board.currentPlayer = Player.O
    else:
        board.currentPlayer = Player.X


def testGame(board: Board):
    print("Primer neispravnog unosa:")
    testRound(board, ('A', 4, Direction.D))
    testRound(board, ('t', 4, Direction.D))
    testRound(board, ('A', 45, Direction.D))
    testRound(board, (1, 4, Direction.D))

    print("Test game:")
    testRound(board, ('A', 1, Direction.DL))
    testRound(board, ('A', 1, Direction.DD))
    testRound(board, ('B', 1, Direction.D))
    testRound(board, ('B', 1, Direction.DD))
    testRound(board, ('C', 1, Direction.D))
    testRound(board, ('A', 2, Direction.DL))
    testRound(board, ('A', 3, Direction.DL))
    testRound(board, ('D', 4, Direction.D))

    testRound(board, ('A', 1, Direction.D))
    testRound(board, ('B', 2, Direction.DD))
    testRound(board, ('D', 1, Direction.D))
    testRound(board, ('C', 1, Direction.DD))
    testRound(board, ('E', 1, Direction.D))
    testRound(board, ('D', 1, Direction.DD))
    testRound(board, ('B', 2, Direction.DL))
    testRound(board, ('B', 3, Direction.DL))

    testRound(board, ('C', 3, Direction.DL))
    testRound(board, ('C', 4, Direction.DL))
    testRound(board, ('C', 5, Direction.DL))
    testRound(board, ('C', 6, Direction.DL))

    testRound(board, ('F', 1, Direction.D))
    testRound(board, ('G', 1, Direction.D))
    testRound(board, ('E', 3, Direction.D))

    testRound(board, ('D', 4, Direction.DL))
    testRound(board, ('D', 5, Direction.DL))
    testRound(board, ('D', 6, Direction.DL))
    testRound(board, ('D', 7, Direction.DL))

    testRound(board, ('D', 1, Direction.DD))
    testRound(board, ('D', 2, Direction.DD))
    testRound(board, ('D', 3, Direction.DD))
    testRound(board, ('D', 4, Direction.DD))

    testRound(board, ('B', 3, Direction.DD))
    testRound(board, ('B', 4, Direction.DD))
    testRound(board, ('A', 4, Direction.DD))

    testRound(board, ('C', 3, Direction.DD))
    testRound(board, ('B', 2, Direction.D))
    testRound(board, ('C', 3, Direction.D))
    testRound(board, ('A', 4, Direction.DL))

    testRound(board, ('F', 2, Direction.D))
    testRound(board, ('C', 4, Direction.DL))
    testRound(board, ('A', 2, Direction.DD))
    testRound(board, ('A', 3, Direction.DD))
    testRound(board, ('C', 4, Direction.DL))
    testRound(board, ('C', 4, Direction.DL))
    testRound(board, ('B', 5, Direction.DL))
    testRound(board, ('D', 5, Direction.DL))
    testRound(board, ('C', 4, Direction.DD))
    testRound(board, ('C', 4, Direction.DD))