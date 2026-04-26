from base_classes.Position import Position
from base_classes.board import Board
from base_classes.pieces import Rook, Knight, Bishop, Queen, King, Pawn

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
        
        if not from_figure: 
            raise ValueError('Начальной фигуры для хода нет!')
        
        if from_figure.color != self.current_turn:
            raise ValueError('Сейчас ход другой стороны!')
        
        all_position = from_figure.get_candidate_moves(self.board, from_pos)

        if to_pos not in all_position:
            raise ValueError('На данную клетку невозможно сделать ход!')
        self.board.temporary_move(from_pos, to_pos)
        try:
            if self.shah_checker(from_figure.color):
                raise ValueError('Невозможно сделать ход, король будет под угрозой!')
        finally:
            self.board.remove_temporary_move()

    def check_checkmate_stalemate(self, color=None):
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
    def shah_checker(self, color):
        king_pos = self.board.find_king(color)
        for pos, figure in self.board:
            if figure.color != color and king_pos in figure.get_attacked_moves(self.board, pos):
                return True
        return False
    def can_move_checker(self, color):
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
    
    