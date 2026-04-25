from game import Game
from time import sleep

def main():
    game = Game()
    while True:
        print("\033[2J\033[H", end='')
        game.print_boarder()
        from_pos = input('Введите координату фигуры для хода (A2 | B1 и тп) --> ')
        to_pos = input('Введите координату куда походить? --> ')
        try:
            game.make_move(from_pos, to_pos)
        except Exception as e:
            print("\033[2J\033[H", end='')
            print(e)
            sleep(2)

if __name__ == '__main__':
    main()