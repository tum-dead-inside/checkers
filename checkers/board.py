from checkers.rules import Checker, PieceType
from checkers.constants import WHITE_PIECES, BLACK_PIECES


class Board:
    def __init__(self, x_size: int, y_size: int):
        self.__x_size = x_size
        self.__y_size = y_size
        self.__generate()

    @property
    def x_size(self) -> int:
        return self.__x_size

    @property
    def y_size(self) -> int:
        return self.__y_size

    @property
    def size(self) -> int:
        return max(self.x_size, self.y_size)

    @classmethod
    def copy(cls, board_instance):
        """Creates a copy of the board from the template"""
        board_copy = cls(board_instance.x_size, board_instance.y_size)

        for y in range(board_instance.y_size):
            for x in range(board_instance.x_size):
                board_copy.at(x, y).change_type(board_instance.type_at(x, y))

        return board_copy

    def __generate(self):
        """Generates a board with all the pieces in their initial positions"""
        self.__checkers = [
            [Checker() for _ in range(self.x_size)] for _ in range(self.y_size)
        ]

        for y, row in enumerate(self.__checkers):
            for x, checker in enumerate(row):
                if (y + x) % 2:
                    if y < 2:
                        checker.change_type(PieceType.BLACK_PIECE)
                    elif y >= self.y_size - 2:
                        checker.change_type(PieceType.WHITE_PIECE)

    def type_at(self, x: int, y: int) -> PieceType:
        """Gets the type of checker on the board at the given coordinates"""
        return self.__checkers[y][x].type

    def at(self, x: int, y: int) -> Checker:
        """Gets the checker on the board at the given coordinates"""
        return self.__checkers[y][x]

    def is_within(self, x: int, y: int) -> bool:
        """Determines if the point is within the board boundaries"""
        return 0 <= x < self.x_size and 0 <= y < self.y_size

    @property
    def white_checkers_count(self) -> int:
        """Number of white pieces on the board"""
        return sum(
            checker.type in WHITE_PIECES for row in self.__checkers for checker in row
        )

    @property
    def black_checkers_count(self) -> int:
        """Number of black pieces on the board"""
        return sum(
            checker.type in BLACK_PIECES for row in self.__checkers for checker in row
        )

    @property
    def white_score(self) -> int:
        """White's score"""
        return sum(
            checker.type == PieceType.WHITE_PIECE
            for row in self.__checkers
            for checker in row
        )

    @property
    def black_score(self) -> int:
        """Black's score"""
        return sum(
            checker.type == PieceType.BLACK_PIECE
            for row in self.__checkers
            for checker in row
        )
