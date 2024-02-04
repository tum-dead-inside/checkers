from enum import Enum


class SideType(Enum):
    """
    Enum representing the side types in a game of checkers.
    """

    WHITE = 1
    BLACK = 2

    @classmethod
    def opposite(cls, side):
        """
        Returns the opposite side of the given side.

        Args:
            side (SideType): The side to get the opposite of.

        Returns:
            SideType: The opposite side.
        """
        return cls.WHITE if side == cls.BLACK else cls.BLACK


class PieceType(Enum):
    """
    Represents the type of a checkers piece.

    Attributes:
        NONE: Represents an empty space on the board.
        WHITE_PIECE: Represents a white checkers piece.
        BLACK_PIECE: Represents a black checkers piece.
    """

    NONE = 1
    WHITE_PIECE = 2
    BLACK_PIECE = 3


class Checker:
    """
    Represents a checker piece in the game of checkers.
    """

    def __init__(self, type: PieceType = PieceType.NONE):
        self.type = type

    def change_type(self, type: PieceType):
        """
        Changes the type of the checker piece.

        Args:
            type (PieceType): The new type of the checker piece.
        """
        self.type = type


class Point:
    def __init__(self, x: int = -1, y: int = -1):
        """
        Initializes a Point object with x and y coordinates.

        Args:
            x (int): The x-coordinate of the point. Default is -1.
            y (int): The y-coordinate of the point. Default is -1.
        """
        self.x = x
        self.y = y

    def __eq__(self, other):
        """
        Checks if two Point objects are equal.

        Args:
            other (Point): The other Point object to compare with.

        Returns:
            bool: True if the two Point objects are equal, False otherwise.
        """
        return isinstance(other, Point) and self.x == other.x and self.y == other.y


class Move:
    """
    Represents a move in a checkers game.

    Attributes:
        from_x (int): The x-coordinate of the starting position.
        from_y (int): The y-coordinate of the starting position.
        to_x (int): The x-coordinate of the destination position.
        to_y (int): The y-coordinate of the destination position.
    """

    def __init__(
        self, from_x: int = -1, from_y: int = -1, to_x: int = -1, to_y: int = -1
    ):
        """
        Initialize a Move object.

        Args:
            from_x (int): The x-coordinate of the starting position.
            from_y (int): The y-coordinate of the starting position.
            to_x (int): The x-coordinate of the destination position.
            to_y (int): The y-coordinate of the destination position.
        """
        self.from_x = from_x
        self.from_y = from_y
        self.to_x = to_x
        self.to_y = to_y

    def __str__(self):
        """
        Returns a string representation of the object.

        The string representation is in the format: "{from_x}-{from_y} -> {to_x}-{to_y}".
        """
        return f"{self.from_x}-{self.from_y} -> {self.to_x}-{self.to_y}"

    def __repr__(self):
        """
        Returns a string representation of the object.

        The string representation includes the coordinates of the starting position
        (from_x, from_y) and the coordinates of the ending position (to_x, to_y).

        Returns:
            str: A string representation of the object.
        """
        return f"{self.from_x}-{self.from_y} -> {self.to_x}-{self.to_y}"

    def __eq__(self, other):
        """
        Check if two Move objects are equal.

        Args:
            other (Move): The other Move object to compare with.

        Returns:
            bool: True if the two Move objects are equal, False otherwise.
        """
        return isinstance(other, Move) and vars(self) == vars(other)
