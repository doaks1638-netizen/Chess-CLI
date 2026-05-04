from base_classes.Position import Position
from base_classes.board import Board
from typing import Literal
from pathlib import Path
from json import dump, dumps, load
from datetime import datetime
import subprocess
import shutil
import sys

class MISING:
    
    def __repr__(self):
        return 'MISING'

MISING = MISING()


class Game:

    def __init__(self):
        self.board = Board()
        self.board.setup_initial_position()
        self.current_turn = 'WHITE'

    def make_move(self, from_pos:str, to_pos:str) -> Literal['PAT', 'SHAH', 'MAT'] | None:
        from_pos = Position.from_notation(from_pos.upper())
        to_pos = Position.from_notation(to_pos.upper())
        
        self.check_valide(from_pos, to_pos)
        
        self.board.apply_move(from_pos, to_pos)
        self.change_turn()

        return self.check_checkmate_stalemate()

    def change_turn(self):
        self.current_turn = 'BLACK' if self.current_turn == 'WHITE' else 'WHITE'
    
    def print_boarder(self):
        self.board.print_board()
        print('\n')
        print(f'Сейчас ходят: {self.get_turn()}')
    
    def check_valide(self, from_pos:Position, to_pos:Position):
        '''
        проверяет только допустимость выбранного хода
        '''
        from_figure = self.board.get_piece(from_pos)
        
        all_position = from_figure.get_candidate_moves(self.board, from_pos)

        if to_pos not in all_position:
            raise ValueError('На данную клетку невозможно сделать ход!')
        self.board.temporary_move(from_pos, to_pos)
        try:
            if self.shah_checker(from_figure.color):
                raise ValueError('Невозможно сделать ход, король будет под угрозой!')
        finally:
            self.board.remove_temporary_move()

    def check_checkmate_stalemate(self, color :Literal['WHITE', 'BLACK'] = None) -> Literal['PAT', 'SHAH', 'MAT'] | None:
        if color is None:
            color = self.current_turn
        shah_status = self.shah_checker(color)
        can_move_status = self.can_move_checker(color)
        if not shah_status and can_move_status:
            return None
        elif not shah_status and not can_move_status:
            return 'PAT'
        elif shah_status and can_move_status:
            return 'SHAH'
        else:
            return 'MAT'
        
    def shah_checker(self, color:Literal['WHITE', 'BLACK']):
        king_pos = self.board.find_king(color)
        for pos, figure in self.board:
            if figure.color != color and king_pos in figure.get_attacked_moves(self.board, pos):
                return True
        return False
    
    def can_move_checker(self, color:Literal['WHITE', 'BLACK']):
        for pos, figure in self.board:
            if figure.color == color and (moves := figure.get_candidate_moves(self.board, pos)):
                for move in moves:
                    self.board.temporary_move(pos, move)
                    try:
                        if not self.shah_checker(color):
                            return True
                    finally:
                        self.board.remove_temporary_move()
        return False
                    
    def get_turn(self):
        return 'белые'if self.current_turn == 'WHITE' else 'черные'
    
    def get_maybe_moves(self, from_pos: Position) -> list[Position]:
        from_pos = Position.from_notation(from_pos.upper())
        from_figure = self.board.get_piece(from_pos)
        if not from_figure:
            raise ValueError('Начальной фигуры для хода нет!')
        if from_figure.color != self.current_turn:
            raise ValueError('Сейчас ход другой стороны!')
        else:
            return from_figure.get_candidate_moves(self.board, from_pos)
        
    def save_json(self, name=MISING):
        if name is MISING:
            name = datetime.now().strftime('%d-%m %H:%M%S')
        file_dir = Path.cwd() / 'old_games'
        file_dir.mkdir(exist_ok=True)
        new_file = file_dir / f"{name}.json"
        new_file.touch()  

        with open(new_file.absolute(), 'w') as file:
            dump(self.board.to_dict(), file, ensure_ascii=False, indent=4)

            return new_file.name
        
    def load_json(self, name):
        file_dir = Path.cwd() / 'old_games'
        if not file_dir.exists():
            raise ValueError('Папка для скачивания не найдена!')
        new_file = file_dir / name
        if not new_file.exists():
            raise ValueError('Файл для скачивания не найдена!')
        with open(new_file.absolute()) as file:
            self.board = Board.from_dict(load(file))
        return new_file.name
    
    def json_base_iterdir(self):
        file_dir = Path.cwd() / 'old_games'
        if not file_dir.exists():
            raise ValueError('Папка для скачивания не найдена!')
        file_list = []
        for file in file_dir.iterdir():
            file_list.append(file.name)
        return file_list

    def show_rules(self):
        file_dir = Path.cwd() / 'resources' / 'rules.md'
        if not file_dir.exists():
            raise ValueError('Нет возможности выдать правила, папка программы поврежденна')
        file_dir = file_dir.absolute()
        if sys.platform.startswith('win'):
            subprocess.run(['notepad', file_dir])
        elif sys.platform.startswith('darwin'):
            subprocess.run(['open', file_dir])
        else:
            if shutil.which('vim'):
                subprocess.run(['vim', file_dir])
            elif shutil.which('less'):
                subprocess.run(['less', file_dir])
            else:
                subprocess.run(['xdg-open', file_dir])