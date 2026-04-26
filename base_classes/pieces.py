from base_classes.Position import Position
from abc import ABC, abstractmethod

class Piece(ABC):
    def __init__(self, color):
        self.color = color
        self.has_move = False
    @abstractmethod
    def get_candidate_moves(self, board, position) -> list[Position]:
        pass
    def __repr__(self):
        return self.white if self.color == 'WHITE' else self.black
    def after_move(self):
        self.has_move = True
    def get_attacked_moves(self, board, position:Position):
        return self.get_candidate_moves(board, position)
class StepPiece(Piece):
    def get_candidate_moves(self, board, position) -> list[Position]:
        move_list = []
        for x, y in self.normal_ways:
            x_pos, y_pos = position.to_numbers()
            x_pos += x
            y_pos += y
            try:
                pos = Position.from_numbers(x_pos, y_pos)
            except ValueError:
                continue
            if (figure := board.get_piece(pos)):
                if figure.color != self.color:
                    move_list.append(pos)
            else:
                move_list.append(pos)
        return move_list

class RayPiece(Piece):
    def get_candidate_moves(self, board, position:Position) -> list[Position]:
        move_list = []
        for x, y in self.normal_ways:
            x_pos, y_pos = position.to_numbers()
            while True:
                x_pos += x
                y_pos += y
                try:
                    pos = Position.from_numbers(x_pos, y_pos)
                except ValueError:
                    break
                if (figure := board.get_piece(pos)):
                    if figure.color != self.color:
                        move_list.append(pos)
                        break
                    break
                move_list.append(pos)
        return move_list

class Rook(RayPiece):
    normal_ways = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    white = '♜'
    black = '♖'

class Knight(StepPiece):
    normal_ways = [(2, 1), (-2, 1), (-2, -1), (2, -1), (1, 2), (-1, 2), (-1, -2), (1, -2)]
    white = '♞'
    black = '♘'

class Bishop(RayPiece):
    normal_ways = [(-1, -1), (1, 1), (1, -1), (-1, 1)]
    white = '♝'
    black = '♗'
    
class Queen(RayPiece):
    normal_ways = Bishop.normal_ways + Rook.normal_ways
    white = '♛'
    black = '♕'

class King(StepPiece):
    normal_ways = [(1, 0), (0, 1), (-1, 0), (-1, -1), (1, -1), (-1, 1), (0, -1), (1, 1)]
    white = '♚'
    black = '♔'

class Pawn(Piece):
    white = '♟'
    black = '♙'
    def __init__(self, color):
        super().__init__(color)
    def after_move(self):
        self.has_move = True
    def get_candidate_moves(self, board, position) -> list[Position]:
        move_list = []
        x_pos, y_pos = position.to_numbers()
        direction = 1 if self.color == 'WHITE' else -1
        try:
            pos = Position.from_numbers(x_pos + 0, y_pos + direction)
            if board.get_piece(pos) is None:
                if not self.has_move:
                    try:
                        pos_two = Position.from_numbers(x_pos + 0, y_pos + (direction + direction))
                        if board.get_piece(pos_two) is None: 
                            move_list.append(pos_two)
                    except ValueError:
                        pass
                move_list.append(pos)
        except ValueError:
                pass    
        for x, y in [(1, direction), (-1, direction)]:
            try:
                pos = Position.from_numbers(x_pos + x, y_pos + y)
                if (figure := board.get_piece(pos)) is not None:
                    if figure.color != self.color:
                        move_list.append(pos)
            except ValueError:
                pass    
        return move_list
    def get_attacked_moves(self, board, position):
        move_list = []
        x_pos, y_pos = position.to_numbers()
        direction = 1 if self.color == 'WHITE' else -1
        for x, y in [(1, direction), (-1, direction)]:
            try:
                pos = Position.from_numbers(x_pos + x, y_pos + y)
                move_list.append(pos)
            except ValueError:
                pass    
        return move_list