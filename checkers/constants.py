from checkers.rules import Point, PieceType, SideType

# side for which the player starts the game
PLAYER_SIDE = SideType.WHITE

# size of the board
X_SIZE = Y_SIZE = 6
# size of a cell (in pixels)
CELL_SIZE = 75

# animation speed (the higher the value, the faster the animation)
ANIMATION_SPEED = 4

# number of moves used for the AI to predict the best move
MAX_PREDICTION_DEPTH = 1

# border width
BORDER_WIDTH = 2 * 2

# colors of the game board
BOARD_COLORS = ["#393939", "#161616"]
# border color when hovering over a cell with the mouse
HOVER_BORDER_COLOR = "#42be65"
# border color when selecting a cell
SELECT_BORDER_COLOR = "#ee5396"
# color of circles for possible moves
POSIBLE_MOVE_CIRCLE_COLOR = "#ee5396"

# possible move offsets
MOVE_OFFSETS = [Point(-1, -1), Point(1, -1), Point(-1, 1), Point(1, 1)]

# arrays of types for white and black pieces [regular piece]
# using an array to make it easier to add new types of pieces (e.g. king)
WHITE_PIECES = [PieceType.WHITE_PIECE]
BLACK_PIECES = [PieceType.BLACK_PIECE]

# constants for RL
LEARNING_RATE = 0.001
BATCH_SIZE = 64
GAMMA = 0.99
EPSILON = 0.1
REPLAY_BUFFER_SIZE = 10000
