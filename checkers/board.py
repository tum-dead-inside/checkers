from checkers.rules import Checker, PieceType
from checkers.constants import WHITE_PIECES, BLACK_PIECES


class Board:
    """Represents a checkers board"""

    def __init__(self, x_size: int, y_size: int):
        """
        Initializes a new instance of the Board class.

        Args:
            x_size (int): The size of the board along the x-axis.
            y_size (int): The size of the board along the y-axis.
        """
        self.__x_size = x_size
        self.__y_size = y_size
        self.__generate()

    @property
    def x_size(self) -> int:
        """
        Get the size of the board along the x-axis.

        Returns:
            int: The size of the board along the x-axis.
        """
        return self.__x_size

    @property
    def y_size(self) -> int:
        """
        Get the size of the board in the y-direction.

        Returns:
            int: The size of the board in the y-direction.
        """
        return self.__y_size

    @property
    def size(self) -> int:
        """
        Returns the maximum size of the board, which is determined by the larger dimension (x or y).

        Returns:
            int: The maximum size of the board.
        """
        return max(self.x_size, self.y_size)

    @classmethod
    def copy(cls, board_instance):
        """
        Creates a copy of the board from the template.

        Parameters:
            board_instance (Board): The board instance to be copied.

        Returns:
            Board: A new board instance that is a copy of the original board.
        """
        board_copy = cls(board_instance.x_size, board_instance.y_size)

        for y in range(board_instance.y_size):
            for x in range(board_instance.x_size):
                board_copy.at(x, y).change_type(board_instance.type_at(x, y))

        return board_copy

    def __generate(self):
        """
        Generate the checkers board by initializing the checkers array and assigning piece types to each checker.

        The checkers array is a 2D list representing the checkers board.
        Each element in the array is an instance of the Checker class.

        The piece types are assigned based on the position of the checker on the board.
        Checkers in the top two rows are assigned the PieceType.BLACK_PIECE type.
        Checkers in the bottom two rows are assigned the PieceType.WHITE_PIECE type.
        """
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
        """Gets the type of checker on the board at the given coordinates.

        Args:
            x (int): The x-coordinate of the checker.
            y (int): The y-coordinate of the checker.

        Returns:
            PieceType: The type of checker at the given coordinates.
        """
        return self.__checkers[y][x].type

    def at(self, x: int, y: int) -> Checker:
        """Gets the checker on the board at the given coordinates

        Args:
            x (int): The x-coordinate of the checker
            y (int): The y-coordinate of the checker

        Returns:
            Checker: The checker at the given coordinates
        """
        return self.__checkers[y][x]

    def is_within(self, x: int, y: int) -> bool:
        """
        Determines if the point is within the board boundaries.

        Args:
            x (int): The x-coordinate of the point.
            y (int): The y-coordinate of the point.

        Returns:
            bool: True if the point is within the board boundaries, False otherwise.
        """
        return 0 <= x < self.x_size and 0 <= y < self.y_size

    @property
    def white_checkers_count(self) -> int:
        """
        Returns the count of white checkers on the board.

        Returns:
            int: The count of white checkers.
        """
        return sum(
            checker.type in WHITE_PIECES for row in self.__checkers for checker in row
        )

    @property
    def black_checkers_count(self) -> int:
        """
        Returns the count of black checkers on the board.

        Returns:
            int: The count of black checkers.
        """
        return sum(
            checker.type in BLACK_PIECES for row in self.__checkers for checker in row
        )

    @property
    def white_score(self) -> int:
        """
        Calculates the score of white pieces on the board.

        Returns:
            The total number of white pieces on the board.
        """
        return sum(
            checker.type == PieceType.WHITE_PIECE
            for row in self.__checkers
            for checker in row
        )

    @property
    def black_score(self) -> int:
        """
        Calculates the score of black pieces on the board.

        Returns:
            int: The number of black pieces on the board.
        """
        return sum(
            checker.type == PieceType.BLACK_PIECE
            for row in self.__checkers
            for checker in row
        )
