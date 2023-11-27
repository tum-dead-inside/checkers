
import numpy as np




class checkers_env:

    def __init__(self, board, player):

        self.board = board
        self.player = player

    def reset(self):
        self.board = [[ 1,0,1,0,1,0],
                      [ 0,1,0,1,0,1],
                      [ 0,0,0,0,0,0],
                      [ 0,0,0,0,0,0],
                      [ 0,-1,0,-1,0,-1],
                      [-1,0,-1,0,-1,0]]
        self.player = 1

    def possible_pieces(self, player):
        positions = []
        for i, row in enumerate(self.board):
            for j, value in enumerate(row):
                if value == player:
                    positions.append([i,j])
        return positions

    def possible_actions(self, player):
        def is_valid_position(x, y):
            return 0 <= x < 6 and 0 <= y < 6
        actions = []
        starters = self.possible_pieces(player)
        directions = [(1, -1), (1, 1)] if player == 1 else [(-1, -1), (-1, 1)]
        for x,y in starters:
            for dx, dy in directions:
                nx, ny = x+dx, y+dy
                if is_valid_position(nx, ny):
                    if self.board[nx][ny] == 0:
                    # one-step
                        actions.append([x,y,nx,ny])
                    elif self.board[nx][ny] == -player:
                    # one jump
                        jx, jy = x+2*dx, y+x*dy
                        if is_valid_position(jx, jy):
                            if self.board[jx][jy] == 0:
                                actions.append([x,y,jx,jy])
        return actions


    def get_piece(self, action):
        if action[2] - action [0] > 1:
            # jump
            self.board[(action[0]+action[2])/2][(action[1]+action[3])/2] = 0

    def game_winner(self):
        if np.sum(self.board<0) == 0:
            return 1
        elif np.sum(self.board>0) == 0:
            return -1
        elif len(self.possible_actions(-1)) == 0:
            return -1
        elif len(self.possible_actions(1)) == 0:
            return 1
        else:
            return 0

    def step(self, action, player):
        row1, co1, row2, co2 = action
        if action in self.possible_actions(player):
            self.board[row1][co1] = 0
            self.board[row2][co2] = player
            self.get_piece(action)
            if self.game_winner() == player:
                reward = 1
            else:
                reward = 0
        else:
            reward = 0

        return reward

    def render(self):
        for row in self.board:
            for square in row:
                if square == 1:
                    piece = "|0"
                elif square == -1:
                    piece = "|X"
                else:
                    piece = "| "
                print(piece, end='')
            print("|")