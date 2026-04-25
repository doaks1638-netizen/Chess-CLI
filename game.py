from Position import Position
from board import Board
from pieces import Rook, Knight, Bishop, Queen, King, Pawn

class Game:
    def __init__(self):
        self.board = Board()
        self.board.setup_initial_position()
        self.current_turn = 'WHITE'
    def make_move(self, from_pos, to_pos):
        from_pos = Position.from_notation(from_pos.upper())
        to_pos = Position.from_notation(to_pos.upper())
        from_figure = self.board.get_piece(from_pos)

        if from_figure.color != self.current_turn:
            raise ValueError('Сейчас ход другой стороны!')
        
        if not from_figure: 
            raise KeyError('Начальной фигуры для хода нет!')
        
        if to_pos not in from_figure.get_candidate_moves(self.board, from_pos):
            raise KeyError('На данную клетку невозможно сделать ход!')
        
        self.board.apply_move(from_pos, to_pos)
        self.change_turn()

    def change_turn(self):
        self.current_turn = 'BLACK' if self.current_turn == 'WHITE' else 'WHITE'
    
    def print_boarder(self):
        self.board.print_board()
        print('\n')
        print(f'Сейчас ходят: {self.current_turn}')
    