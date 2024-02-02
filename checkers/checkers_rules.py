class CheckersRules:
    def __init__(self, board):
        self.board = board

    def is_valid_move(self, start, end):
        start_x, start_y = start
        end_x, end_y = end

        # check that the start and end coordinates are on the board
        if not (0 <= start_x < 8 and 0 <= start_y < 8 and 0 <= end_x < 8 and 0 <= end_y < 8):
            return False

        # check that the start coordinate contains a piece
        if self.board[start_y][start_x] == " ":
            return False

        # check that the end coordinate is empty
        if self.board[end_y][end_x] != " ":
            return False

        # check that the move is diagonal
        if abs(start_x - end_x) != abs(start_y - end_y):
            return False

        return True
    
    def get_valid_moves(self, player, row, col):
        moves = []
        if player == "W":
            if row > 0 and col > 0 and self.board[row - 1][col - 1] == " ":
                moves.append((row - 1, col - 1))
            if row > 0 and col < 7 and self.board[row - 1][col + 1] == " ":
                moves.append((row - 1, col + 1))
        else:
            if row < 7 and col > 0 and self.board[row + 1][col - 1] == " ":
                moves.append((row + 1, col - 1))
            if row < 7 and col < 7 and self.board[row + 1][col + 1] == " ":
                moves.append((row + 1, col + 1))
        return moves
        
        