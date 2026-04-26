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
        
        self.check_valide(from_pos, to_pos)
        
        self.board.apply_move(from_pos, to_pos)
        self.change_turn()

    def change_turn(self):
        self.current_turn = 'BLACK' if self.current_turn == 'WHITE' else 'WHITE'
    
    def print_boarder(self):
        self.board.print_board()
        print('\n')
        print(f'Сейчас ходят: {'белые' if self.current_turn == 'WHITE' else 'черные'}')
    
    def check_valide(self, from_pos:Position, to_pos:Position):
        '''
        проверяет только допустимость выбранного хода
        '''
        king_pos = self.board.find_king()
        from_figure = self.board.get_piece(from_pos)

        if from_figure.color != self.current_turn:
            raise ValueError('Сейчас ход другой стороны!')
        
        if not from_figure: 
            raise ValueError('Начальной фигуры для хода нет!')
        
        if to_pos not in from_figure.get_candidate_moves(self.board, from_pos):
            raise ValueError('На данную клетку невозможно сделать ход!')
        

    def check_checkmate_stalemate(self):
        '''
        проверяет шах / мат / пат после уже сделанного хода
        '''
    