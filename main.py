from base_classes.game import Game
from time import sleep

def main():

    game = Game()

    while True:
        print("\033[2J\033[H", end='')
        game.print_boarder()
        from_pos = input('Введите координату фигуры для хода --> ')
        to_pos = input('Введите координату куда походить? --> ')

        try:
            status = game.make_move(from_pos, to_pos)
            match status:

                case 'PAT':
                    for _ in range(3):
                        print("\033[2J\033[H", end='')
                        print(f'ИГРА ОКОНЧЕНА! ПАТ на стороне {game.get_turn()}')
                        sleep(1)
                    break

                case 'SHAH':
                    for _ in range(3):
                        print("\033[2J\033[H", end='')
                        print(f'ВНИМАНИЕ! ШАХ на стороне {game.get_turn()}')
                        sleep(1)
                case 'MAT':
                    
                    for _ in range(3):
                        print("\033[2J\033[H", end='')
                        print(f'ИГРА ОКОНЧЕНА! МАТ на стороне {game.get_turn()}')
                        sleep(1)
                    break
                        
        except Exception as e:
            print("\033[2J\033[H", end='')
            print(e)
            sleep(2)

if __name__ == '__main__':
    main()