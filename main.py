from board import Board
from enums import Player
from test import testGame

def main():
    try:
        board = Board(True, 4, Player.O) #True - da li igra kompjuter, 4 - Velicina table, Player.O - Ko prvi igra
        board.initialize()

        print("Inicijalno stanje:")
        board.print()

        testGame(board)

        board.print()
        print(f"Poeni igraca X: {board.xPoints}")
        print(f"Poeni igraca O: {board.oPoints}")
    except Exception as e:
        print(f"Greška: {e}")

if __name__ == "__main__":
    main()