from pieces import Rook, Knight, Bishop, Queen, King, Pawn
from Position import Position

class Board:
    pieces = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
    cords = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    def __init__(self):
        self.board = {}
        self.history = []
    def get_piece(self, pos):
        return self.board.get(pos, None)
    def find_king(self, color):
        for pos, piece in self.board.items():
            if piece.name == 'King' and piece.color == color:
                return pos
    def apply_move(self, from_pos, to_pos):
        self.board[to_pos] = self.board.pop(from_pos)
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
    def __iter__(self):
        yield from self.board.items()
    def temporary_move(self, from_pos, to_pos):
        from_pos = self.board.pop(from_pos)
        self.board[to_pos] = from_pos
        self.history.append(from_pos, to_pos)
    def remove_temporary_move(self):
        from_pos, to_pos = self.history.pop()
        self.board[from_pos] = self.board.pop(to_pos)