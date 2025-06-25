from game import Game, clear_console
from enums import Player

def main():
    try:
        clear_console()        
        
        while True:
            izbor = input('Izaberite mod igre:\n1 - Igrac protiv racunara\n0 - Igrac protiv igraca\n').strip()
            if izbor in ('0', '1'):
                isComputerPlaying = bool(int(izbor))
                break
            else:
                print("Unos mora biti 0 ili 1. Pokušajte ponovo.")      
                
        while True:
            tableSize = int(input('Unesite velicinu table (4-8): ').strip())
            if 4 <= tableSize <= 8:
                break
            else:
                print("Veličina table mora biti između 4 i 8.")

        
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