from base_classes.game import Game
from time import sleep
import os

def show_menu():
    print("""
 ██████╗██╗  ██╗███████╗███████╗███████╗
██╔════╝██║  ██║██╔════╝██╔════╝██╔════╝
██║     ███████║█████╗  ███████╗███████╗
██║     ██╔══██║██╔══╝  ╚════██║╚════██║
╚██████╗██║  ██║███████╗███████║███████║
 ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝

    ♙  A terminal chess experience  ♟
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

           ─── MAIN MENU ───

  [1]  ♔  Новая игра
  [2]  ♖  Импортировать из файла
  [3]  ♔  Прочитать правила игры 
  [4]  ♖  Справка 

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━""")
    

def chess_game(game: Game):
    clear_t()
    while True:
        try:
            clear_t()
            game.print_boarder()
            if game.step_50_rules():
                draw_stat = input('Правило 50 ходов. Чтобы не затягивать партию до бесконечности,' \
                ' предлогаем вам объевить ничью. y/n --> ')
                match draw_stat:
                    case 'y':
                        for _ in range(3):
                            clear_t()
                            print('ИГРА ОКОНЧЕНА! Ничья между игроками')
                            sleep(1)
                        break
                    case _:
                        clear_t()
                        game.print_boarder()
            from_pos = input('Введите координату фигуры для хода --> ')
            try:
                moves = game.get_maybe_moves(from_pos)
                print(f'Доступные ходы: {' ,'.join(map(str, moves))}')
            except Exception as e:
                clear_t()
                print(e)
                sleep(2)
                continue
            to_pos = input('Введите координату куда походить? --> ')

            try:
                status = game.make_move(from_pos, to_pos)
                match status:

                    case 'PAT':
                        for _ in range(3):
                            clear_t()
                            print(f'ИГРА ОКОНЧЕНА! ПАТ на стороне {game.get_turn()}')
                            sleep(1)
                        break

                    case 'SHAH':
                        for _ in range(3):
                            clear_t()
                            print(f'ВНИМАНИЕ! ШАХ на стороне {game.get_turn()}')
                            sleep(1)
                    case 'MAT':

                        for _ in range(3):
                            clear_t()
                            print(f'ИГРА ОКОНЧЕНА! МАТ на стороне {game.get_turn()}')
                            sleep(1)
                        break
                            
            except Exception as e:
                clear_t()
                print(e)
                sleep(2)
        except KeyboardInterrupt:
            try:
                save_choise = input('\n\nХотели ли бы вы сделать копию игры? Сохранится в вашей домашней дириктории. y/n --> ')
                if save_choise == 'y':
                    name = input('\n\nВведите имя для сохранения... Дефолт - текущая дата --> ')
                    if name:
                        file_save_name = game.save_json(name)
                        print(f'\nСохранено в {file_save_name}! ✅')
                    else:
                        file_save_name = game.save_json()
                        print(f'\nСохранено в {file_save_name}! ✅')
                print('\n\nBye!👀')
                break
            except KeyboardInterrupt:
                print('\n\nBye!👀')
                break

def menu():
    game = Game()

    while True:
        try:
            
            clear_t()
            show_menu()
            choice = input('Выберите пункт меню: -> ')

            if choice == '1':
                chess_game(game)
                return
            if choice == '2':
                print('\nСписок доступных партий:\n')
                list_of_files = game.json_base_iterdir()
                for num, filename in enumerate(list_of_files, 1):
                    print(f'{num}. - {filename}')
                print()
                try:
                    name_choice = input('Введите номер файла для старта -> ')
                    if not (name_choice.isdigit() and (int(name_choice) - 1) < len(list_of_files)):
                        raise ValueError('Неверное выбран файл!')
                    name_choice = int(name_choice) - 1
                    file_save_name = game.load_json(list_of_files[name_choice])
                    print(f'\n\nУспешно импортировано из {file_save_name}!')
                    chess_game(game)
                    return
                except ValueError as e:
                    print(f'\n\nВозникла ошибка -> {e}')
                    choice_result = input('\nCоздать новую игру? y|n -> ')
                    if choice_result != 'y':
                        print('\n\nBye!👀')
                        return
                    else:
                        chess_game(game)
                        return
                except Exception as e:
                    print('Возникла неизвестная ошибка! :(')
                    return
            elif choice == '3':
                game.show_resources_file('rules.md')
            elif choice == '4':
                game.show_resources_file('possibilities.md')
        except KeyboardInterrupt:
            print('\n\nBye!👀')
            return
        clear_t()

def clear_t():
    os.system('cls' if os.name == 'nt' else 'clear')
    
if __name__ == '__main__':
    menu()