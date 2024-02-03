from enum import Enum


class SideType(Enum):
    WHITE = 1
    BLACK = 2

    @classmethod
    def opposite(cls, side):
        return cls.WHITE if side == cls.BLACK else cls.BLACK


class PieceType(Enum):
    NONE = 1
    WHITE_PIECE = 2
    BLACK_PIECE = 3


class Checker:
    def __init__(self, type: PieceType = PieceType.NONE):
        self.type = type

    def change_type(self, type: PieceType):
        """Change the type of the piece"""
        self.type = type


class Point:
    def __init__(self, x: int = -1, y: int = -1):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return isinstance(other, Point) and self.x == other.x and self.y == other.y


class Move:
    def __init__(
        self, from_x: int = -1, from_y: int = -1, to_x: int = -1, to_y: int = -1
    ):
        self.from_x = from_x
        self.from_y = from_y
        self.to_x = to_x
        self.to_y = to_y

    def __str__(self):
        return f"{self.from_x}-{self.from_y} -> {self.to_x}-{self.to_y}"

    def __repr__(self):
        return f"{self.from_x}-{self.from_y} -> {self.to_x}-{self.to_y}"

    def __eq__(self, other):
        return isinstance(other, Move) and vars(self) == vars(other)
