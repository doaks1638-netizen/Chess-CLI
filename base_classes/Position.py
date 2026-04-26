from re import fullmatch

class Position:
    bkv = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    def __init__(self, x, y):
        self.x_pos = x
        self.y_pos = y
    @property
    def x_pos(self):
        return self._x
    @x_pos.setter
    def x_pos(self, value):
        if value not in {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'}:
            raise ValueError('Данные для X position не корректны')
        self.__dict__['_x'] = value
    @property
    def y_pos(self):
        return self._y
    @y_pos.setter
    def y_pos(self, value):
        if value not in {1, 2, 3, 4, 5, 6, 7, 8}:
            raise ValueError('Данные для Y position не корректны')
        self.__dict__['_y'] = value
    @classmethod
    def from_notation(cls, value):
        if not (isinstance(value, str) and fullmatch(r'[A-H][1-8]', value)):
            raise ValueError('Нет возможности чтения такого типа координат')
        return Position(value[0], int(value[1]))
    def to_notation(self):
        return f'{self.x_pos}{self.y_pos}'
    def __repr__(self):
        return f'Position({self.x_pos}, {self.y_pos})'
    def __eq__(self, other):
        if not isinstance(other, Position):
            return NotImplemented
        return (self.x_pos, self.y_pos) == (other.x_pos, other.y_pos)
    def __hash__(self):
        return hash((self.x_pos, self.y_pos))
    def check_cell_color(self):
        return 'BLACK' if ((self.y_pos + ord(self.x_pos) - 64) % 2 == 0) else 'WHITE'
    def to_numbers(self):
        return (ord(self.x_pos) - 64, self.y_pos)
    @classmethod
    def from_numbers(cls, x, y):
        if 0 < x < 9 and 0 < y < 9:
            return Position(cls.bkv[x - 1], y)
        raise ValueError('Неправильный тип координат!')