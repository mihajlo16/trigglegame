from game import Game
from enums import Player

def main():
    #try:
        game = Game(True, 7, Player.O) #True - da li igra kompjuter, 4 - Velicina table, Player.O - Ko prvi igra
        game.startGame()
    #except Exception as e:
    #    print(f"Greška: {e}")

if __name__ == "__main__":
    main()