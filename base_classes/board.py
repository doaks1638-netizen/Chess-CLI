from base_classes.pieces import Rook, Knight, Bishop, Queen, King, Pawn
from base_classes.Position import Position
from typing import Literal, Iterable

class Board:
    pieces = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
    cords = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    def __init__(self):
        self.board = {}
        self.history = [] # история для временных ходов (в будущем будет изменена логика на сохранение кодов)

    def get_piece(self, pos:Position):
        return self.board.get(pos, None)
    
    def find_king(self, color:Literal['WHITE', 'BLACK']):
        for pos, piece in self.board.items():
            if isinstance(piece, King) and piece.color == color:
                return pos
        raise ValueError('Король не найден! Если была загрузка через json, пожалуйста не ломайте фигуры!')
    
    def apply_move(self, from_pos:Position, to_pos:Position):
        piece = self.board.pop(from_pos)
        self.board[to_pos] = piece
        piece.after_move()

    def setup_initial_position(self):
        self.board.clear()
        for piece, cord in zip(self.pieces, self.cords):
            self.board[Position(cord, 1)] = piece('WHITE')
            self.board[Position(cord, 2)] = Pawn('WHITE')
            self.board[Position(cord, 7)] = Pawn('BLACK')
            self.board[Position(cord, 8)] = piece('BLACK')

    def print_board(self):
        for n in range(8,0, -1):
            stack = ''
            for let in self.cords:
                cell = Position(let, n)
                color = cell.check_cell_color()
                stack += f"{(self.board.get(cell, '▢' if color == 'BLACK' else '■'))} "
            print(f'{n} {stack}')
            stack = ''
        print('  A B C D E F G H')   

    def __iter__(self) -> Iterable:
        yield from self.board.items()

    def temporary_move(self, from_pos:Position, to_pos:Position): # делает ход и запоминает его в истории
        from_piece = self.board.pop(from_pos)
        to_piece = self.board.pop(to_pos, None)
        self.board[to_pos] = from_piece
        self.history.append((from_pos, to_pos, from_piece, to_piece))
        
    def remove_temporary_move(self): # удаляяет прошлый ход из истории возварщая все фигруы
        from_pos, to_pos, from_piece, to_piece = self.history.pop()
        self.board.pop(to_pos)
        self.board[from_pos] = from_piece
        if to_piece is not None:
            self.board[to_pos] = to_piece
    
    def to_dict(self):
        self.normal_dict = dict()
        for key, value in self.board.items():
            self.normal_dict[key.to_json()] = value.to_json()
        return self.normal_dict