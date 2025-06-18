from game import Game, clear_console
from enums import Player

def main():
    try:
        clear_console()
        isComputerPlaying = bool(int(input('Izaberite mod igre:\n1 - Igrac protiv racunara\n0 - Igrac protiv igraca\n')))
        
        tableSize = int(input('Unesite velicinu table: '))
        
        firstPlay = Player(input("Unesi ko igra prvi X ili O (Ukoliko se igra protiv racunara, racunar je X): ").strip().upper())
        
        if firstPlay == Player.N:
            raise ValueError('Dozvoljeni su samo unosi X ili O.')
        
        max_depth = 0
        if isComputerPlaying:
            max_depth = int(input('Izaberite dubinu pretrage racunara: '))
        
        clear_console()
        game = Game(isComputerPlaying, tableSize, firstPlay, max_depth)
        game.startGame()
    except ValueError as e:
        print(f"Greška u unosu: {e}")
    except Exception as e:
        print(f"Greška: {e}")

if __name__ == "__main__":
    main()