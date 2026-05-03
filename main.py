from base_classes.game import Game
from time import sleep

def main():

    game = Game()

    while True:
        try:
            print("\033[2J\033[H", end='')
            game.print_boarder()
            from_pos = input('Введите координату фигуры для хода --> ')
            try:
                moves = game.get_maybe_moves(from_pos)
                print(f'Доступные ходы: {' ,'.join(map(str, moves))}')
            except Exception as e:
                print("\033[2J\033[H", end='')
                print(e)
                sleep(2)
                continue
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
        except KeyboardInterrupt:
            try:
                save_choise = input('\n\nХотели ли бы вы сделать копию игры? Сохранится в вашей домашней дириктории. y/n --> ')
                if save_choise == 'y':
                    name = input('\n\nВведите имя для сохранения... Дефолт - текущая дата --> ')
                    if name:
                        game.save_json(name)
                        print('\nСохранено! ✅')
                    else:
                        game.save_json()
                        print('\nСохранено! ✅')
                print('\n\nBye!👀')
                break
            except KeyboardInterrupt:
                print('\n\nBye!👀')
                break
if __name__ == '__main__':
    main()