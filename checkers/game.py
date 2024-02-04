from tkinter import Canvas, Event, messagebox
from PIL import Image, ImageTk
from random import choice
from pathlib import Path
from math import inf
import torch
import torch.optim as optim
from typing import List
import random

from checkers.board import Board
from checkers.rules import Move, PieceType, SideType, Point
from checkers.constants import *
from rl.dqn import DQN, ReplayBuffer, train_dqn
from rl.experience import Experience


class Game:
    def __init__(self, canvas: Canvas, x_board_size: int, y_board_size: int):
        """
        Initializes a new instance of the Game class.

        Args:
            canvas (Canvas): The canvas object to draw the game on.
            x_board_size (int): The number of columns on the game board.
            y_board_size (int): The number of rows on the game board.
        """
        self.__canvas = canvas
        self.__board = Board(x_board_size, y_board_size)

        # DQN and ReplayBuffer setup
        input_size = x_board_size * y_board_size
        output_size = len(MOVE_OFFSETS)
        self.dqn = DQN(input_size, output_size)
        self.optimizer = optim.Adam(self.dqn.parameters(), lr=LEARNING_RATE)
        self.replay_buffer = ReplayBuffer(REPLAY_BUFFER_SIZE)

        self.__player_turn = True

        self.__hovered_cell = Point()
        self.__selected_cell = Point()
        self.__animated_cell = Point()

        self.__init_images()

        self.__draw()

        if PLAYER_SIDE == SideType.BLACK:
            self.__handle_enemy_turn()


class Game:
    def __init__(self, canvas: Canvas, x_board_size: int, y_board_size: int):
        """
        Initializes a new instance of the Game class.

        Args:
            canvas (Canvas): The canvas object to draw the game on.
            x_board_size (int): The number of columns on the game board.
            y_board_size (int): The number of rows on the game board.
        """
        self.__canvas = canvas
        self.__board = Board(x_board_size, y_board_size)

        # DQN and ReplayBuffer setup
        input_size = x_board_size * y_board_size
        output_size = len(MOVE_OFFSETS)
        self.dqn = DQN(input_size, output_size)
        self.optimizer = optim.Adam(self.dqn.parameters(), lr=LEARNING_RATE)
        self.replay_buffer = ReplayBuffer(REPLAY_BUFFER_SIZE)

        self.__player_turn = True

        self.__hovered_cell = Point()
        self.__selected_cell = Point()
        self.__animated_cell = Point()

        self.__init_images()

        self.__draw()

        if PLAYER_SIDE == SideType.BLACK:
            self.__handle_enemy_turn()

    def __init_images(self):
        """Initialize images.

        This method initializes the images used in the game. It creates a dictionary
        of images, where the keys are the piece types (WHITE_PIECE and BLACK_PIECE)
        and the values are the corresponding image objects.

        Returns:
            None
        """
        self.__images = {
            PieceType.WHITE_PIECE: ImageTk.PhotoImage(
                Image.open(Path("assets", "white-piece.png")).resize(
                    (CELL_SIZE, CELL_SIZE)
                )
            ),
            PieceType.BLACK_PIECE: ImageTk.PhotoImage(
                Image.open(Path("assets", "black-piece.png")).resize(
                    (CELL_SIZE, CELL_SIZE)
                )
            ),
        }

    def __animate_move(self, move: Move):
        """Animate the piece's movement

        Args:
            move (Move): The move object representing the piece's movement.

        Returns:
            None
        """
        self.__animated_cell = Point(move.from_x, move.from_y)
        self.__draw()

        # create a piece for the animation
        animated_piece = self.__canvas.create_image(
            move.from_x * CELL_SIZE,
            move.from_y * CELL_SIZE,
            image=self.__images.get(self.__board.type_at(move.from_x, move.from_y)),
            anchor="nw",
            tag="animated_piece",
        )

        # movement vectors
        dx = 1 if move.from_x < move.to_x else -1
        dy = 1 if move.from_y < move.to_y else -1

        # animation loop
        for _distance in range(abs(move.from_x - move.to_x)):
            for _ in range(100 // ANIMATION_SPEED):
                self.__canvas.move(
                    animated_piece,
                    ANIMATION_SPEED / 100 * CELL_SIZE * dx,
                    ANIMATION_SPEED / 100 * CELL_SIZE * dy,
                )
                self.__canvas.update()

        self.__animated_cell = Point()

    def __draw(self):
        """Draw the board grid and the pieces"""
        self.__canvas.delete("all")
        self.__draw_board_grid()
        self.__draw_pieces()

    def __draw_board_grid(self):
        """Draw the board grid.

        This method is responsible for drawing the grid of the game board on the canvas.
        It iterates over each cell in the board and creates rectangles to represent the cells.
        The color of each cell is determined by the BOARD_COLORS list.
        If a cell is selected or hovered, a border is drawn around it using the SELECT_BORDER_COLOR or HOVER_BORDER_COLOR.
        If a cell is selected, possible move circles are drawn on the cells where the player can move.

        Args:
            None

        Returns:
            None
        """
        for y in range(self.__board.y_size):
            for x in range(self.__board.x_size):
                self.__canvas.create_rectangle(
                    x * CELL_SIZE,
                    y * CELL_SIZE,
                    x * CELL_SIZE + CELL_SIZE,
                    y * CELL_SIZE + CELL_SIZE,
                    fill=BOARD_COLORS[(y + x) % 2],
                    width=0,
                    tag="boards",
                )

                # draw borders around the selected and hovered cells
                if x == self.__selected_cell.x and y == self.__selected_cell.y:
                    self.__canvas.create_rectangle(
                        x * CELL_SIZE + BORDER_WIDTH // 2,
                        y * CELL_SIZE + BORDER_WIDTH // 2,
                        x * CELL_SIZE + CELL_SIZE - BORDER_WIDTH // 2,
                        y * CELL_SIZE + CELL_SIZE - BORDER_WIDTH // 2,
                        outline=SELECT_BORDER_COLOR,
                        width=BORDER_WIDTH,
                        tag="border",
                    )
                elif x == self.__hovered_cell.x and y == self.__hovered_cell.y:
                    self.__canvas.create_rectangle(
                        x * CELL_SIZE + BORDER_WIDTH // 2,
                        y * CELL_SIZE + BORDER_WIDTH // 2,
                        x * CELL_SIZE + CELL_SIZE - BORDER_WIDTH // 2,
                        y * CELL_SIZE + CELL_SIZE - BORDER_WIDTH // 2,
                        outline=HOVER_BORDER_COLOR,
                        width=BORDER_WIDTH,
                        tag="border",
                    )

                # draw possible move circles if a cell is selected
                if self.__selected_cell:
                    player_moves_list = self.__get_moves_list(PLAYER_SIDE)
                    for move in player_moves_list:
                        if (
                            self.__selected_cell.x == move.from_x
                            and self.__selected_cell.y == move.from_y
                        ):
                            self.__canvas.create_oval(
                                move.to_x * CELL_SIZE + CELL_SIZE / 3,
                                move.to_y * CELL_SIZE + CELL_SIZE / 3,
                                move.to_x * CELL_SIZE + (CELL_SIZE - CELL_SIZE / 3),
                                move.to_y * CELL_SIZE + (CELL_SIZE - CELL_SIZE / 3),
                                fill=POSIBLE_MOVE_CIRCLE_COLOR,
                                width=0,
                                tag="posible_move_circle",
                            )

    def __draw_pieces(self):
        """Draw the pieces on the board.

        This method iterates over the cells of the board and draws the pieces on the canvas.
        It skips drawing empty cells and the animated piece.

        Args:
            None

        Returns:
            None
        """
        for y in range(self.__board.y_size):
            for x in range(self.__board.x_size):
                # don't draw empty cells and the animated piece
                if self.__board.type_at(x, y) != PieceType.NONE and not (
                    x == self.__animated_cell.x and y == self.__animated_cell.y
                ):
                    self.__canvas.create_image(
                        x * CELL_SIZE,
                        y * CELL_SIZE,
                        image=self.__images.get(self.__board.type_at(x, y)),
                        anchor="nw",
                        tag="pieces",
                    )

    def mouse_move(self, event: Event):
        """Mouse move event"""
        x, y = (event.x) // CELL_SIZE, (event.y) // CELL_SIZE
        if x != self.__hovered_cell.x or y != self.__hovered_cell.y:
            self.__hovered_cell = Point(x, y)

            # redraw the board if it's the player's turn
            if self.__player_turn:
                self.__draw()

    def mouse_down(self, event: Event):
        """Handles the mouse click event.

        Args:
            event (Event): The mouse click event.

        Returns:
            None
        """
        if not (self.__player_turn):
            return

        x, y = (event.x) // CELL_SIZE, (event.y) // CELL_SIZE

        # if the point is not within the board
        if not (self.__board.is_within(x, y)):
            return

        if PLAYER_SIDE == SideType.WHITE:
            player_pieces = WHITE_PIECES
        elif PLAYER_SIDE == SideType.BLACK:
            player_pieces = BLACK_PIECES
        else:
            return

        # if the player clicks on one of its pieces, select it
        if self.__board.type_at(x, y) in player_pieces:
            self.__selected_cell = Point(x, y)
            self.__draw()
        elif self.__player_turn:
            move = Move(self.__selected_cell.x, self.__selected_cell.y, x, y)

            # if the player clicks on a cell the selected piece can move to
            if move in self.__get_moves_list(PLAYER_SIDE):
                self.__handle_player_turn(move)
                self.__update_replay_buffer()
                self.__train_dqn()

                if not (self.__player_turn):
                    self.__handle_enemy_turn()

    def __update_replay_buffer(self):
        """Update the replay buffer with the current state, action, reward, and next state.

        This method converts the current state, action, reward, and next state into tensors and adds them to the replay buffer.
        """
        # convert the current state, action, reward, and next state to tensors
        state = torch.tensor([self.__get_flattened_state()], dtype=torch.float32)
        action = torch.tensor([self.__selected_action()], dtype=torch.long)
        reward = torch.tensor([self.__calculate_reward()], dtype=torch.float32)
        next_state = torch.tensor([self.__get_flattened_state()], dtype=torch.float32)

        experience = Experience(state, action, reward, next_state)
        self.replay_buffer.push(experience)  # add the experience to the replay buffer

    def __train_dqn(self):
        """ "Train the DQN using the replay buffer"""
        train_dqn(self.dqn, self.replay_buffer, BATCH_SIZE, GAMMA, self.optimizer)

    def __get_flattened_state(self):
        """Get the flattened representation of the current game state.

        Returns:
            list: A list containing the piece types of each position on the board.
        """
        state = []
        for y in range(self.__board.y_size):
            for x in range(self.__board.x_size):
                piece_type = self.__board.type_at(x, y).value
                state.append(piece_type)
        return state

    def __selected_action(self):
        """Select the action with the highest Q-value for the current state.

        Returns:
            int: The index of the selected action.
        """
        # use epsilon-greedy strategy for action selection
        epsilon = EPSILON
        if random.random() < epsilon:
            return random.randint(0, len(MOVE_OFFSETS) - 1)
        else:
            # get the Q-values for the current state
            state = torch.tensor([self.__get_flattened_state()], dtype=torch.float32)
            q_values = self.dqn(state)
            # select the action with the highest Q-value
            return torch.argmax(q_values).item()

    def __calculate_reward(self):
        """Calculate the reward for the current game state"""
        # TODO: calculate the reward based on the current game state
        # the current implementation is just a placeholder
        white_score = self.__board.white_score
        black_score = self.__board.black_score
        if PLAYER_SIDE == SideType.WHITE:
            reward = white_score - black_score
        elif PLAYER_SIDE == SideType.BLACK:
            reward = black_score - white_score
        else:
            reward = 0
        return reward

    def __handle_move(self, move: Move, draw: bool = True) -> bool:
        """Move a piece from one cell to another.

        Args:
            move (Move): The move object containing the coordinates of the piece to be moved.
            draw (bool, optional): Indicates whether to animate and draw the move. Defaults to True.

        Returns:
            bool: True if a piece was killed during the move, False otherwise.
        """
        if draw:
            self.__animate_move(move)

        # change the position of the piece
        self.__board.at(move.to_x, move.to_y).change_type(
            self.__board.type_at(move.from_x, move.from_y)
        )
        self.__board.at(move.from_x, move.from_y).change_type(PieceType.NONE)

        # movement vectors
        dx = -1 if move.from_x < move.to_x else 1
        dy = -1 if move.from_y < move.to_y else 1

        # delete the killed piece
        has_killed_piece = False
        x, y = move.to_x, move.to_y
        while x != move.from_x or y != move.from_y:
            x += dx
            y += dy
            if self.__board.type_at(x, y) != PieceType.NONE:
                self.__board.at(x, y).change_type(PieceType.NONE)
                has_killed_piece = True

        if draw:
            self.__draw()

        return has_killed_piece

    def __handle_player_turn(self, move: Move):
        """Handle the player's turn.

        Args:
            move (Move): The move made by the player.

        Returns:
            None
        """
        self.__player_turn = False

        # check if the player killed a piece
        has_killed_piece = self.__handle_move(move)

        required_moves_list = list(
            filter(
                lambda required_move: move.to_x == required_move.from_x
                and move.to_y == required_move.from_y,
                self.__get_required_moves_list(PLAYER_SIDE),
            )
        )

        # check if the player can move again with the same piece
        if has_killed_piece and required_moves_list:
            self.__player_turn = True

        self.__selected_cell = Point()

    def __handle_enemy_turn(self):
        """Handle the enemy's turn (computer)

        This method is responsible for handling the enemy's turn in the game. It sets the player's turn to False,
        predicts the optimal moves for the enemy using the __predict_optimal_moves method, and then handles each move
        by calling the __handle_move method. After all the moves are handled, it sets the player's turn back to True
        and checks for game over.

        """
        self.__player_turn = False

        optimal_moves_list = self.__predict_optimal_moves(
            SideType.opposite(PLAYER_SIDE)
        )

        for move in optimal_moves_list:
            self.__handle_move(move)

        self.__player_turn = True

        self.__check_for_game_over()

    def __check_for_game_over(self):
        """Check if the game is over.

        This method checks if the game is over by checking if there are any valid moves left for both the white and black sides.
        If there are no valid moves left for either side, the game is considered over and a message box is displayed to indicate the winner.
        If the game is over, a new game is initialized.

        """
        game_over = False

        white_moves_list = self.__get_moves_list(SideType.WHITE)
        if not (white_moves_list):
            # white lost
            messagebox.showinfo("Game Over", "The black pieces won!")
            game_over = True
            exit()

        black_moves_list = self.__get_moves_list(SideType.BLACK)
        if not (black_moves_list):
            # black lost
            messagebox.showinfo("Game Over", "The white pieces won!")
            game_over = True
            exit()

        if game_over:
            # new game
            self.__init__(self.__canvas, self.__board.x_size, self.__board.y_size)

    def __predict_optimal_moves(self, side: SideType) -> list[Move]:
        """Predict the optimal move for the enemy side.

        Args:
            side (SideType): The side for which to predict the optimal move.

        Returns:
            list[Move]: A list of optimal moves.

        """
        best_result = 0
        optimal_moves = []
        predicted_moves_list = self.__get_predicted_moves_list(side)

        if predicted_moves_list:
            board_copy = Board.copy(self.__board)
            for moves in predicted_moves_list:
                for move in moves:
                    self.__handle_move(move, draw=False)

                try:
                    if side == SideType.WHITE:
                        result = self.__board.white_score / self.__board.black_score
                    elif side == SideType.BLACK:
                        result = self.__board.black_score / self.__board.white_score
                except ZeroDivisionError:
                    result = inf

                if result > best_result:
                    best_result = result
                    optimal_moves.clear()
                    optimal_moves.append(moves)
                elif result == best_result:
                    optimal_moves.append(moves)

                self.__board = Board.copy(board_copy)

        optimal_move = []
        if optimal_moves:
            # filter the moves that kills the most pieces
            for move in choice(optimal_moves):
                if (
                    side == SideType.WHITE
                    and self.__board.type_at(move.from_x, move.from_y) in BLACK_PIECES
                ):
                    break
                elif (
                    side == SideType.BLACK
                    and self.__board.type_at(move.from_x, move.from_y) in WHITE_PIECES
                ):
                    break

                optimal_move.append(move)

        return optimal_move

    def __get_predicted_moves_list(
        self,
        side: SideType,
        current_prediction_depth: int = 0,
        all_moves_list: list[Move] = [],
        current_moves_list: list[Move] = [],
        required_moves_list: list[Move] = [],
    ) -> list[Move]:
        """
        Predict all possible moves.

        Args:
            side (SideType): The side for which to predict moves.
            current_prediction_depth (int, optional): The current depth of prediction. Defaults to 0.
            all_moves_list (list[Move], optional): The list to store all predicted moves. Defaults to [].
            current_moves_list (list[Move], optional): The list to store the current moves being considered. Defaults to [].
            required_moves_list (list[Move], optional): The list of required moves for a piece. Defaults to [].

        Returns:
            list[Move]: The list of all predicted moves.
        """
        if current_moves_list:
            all_moves_list.append(current_moves_list)
        else:
            all_moves_list.clear()

        if required_moves_list:
            moves_list = required_moves_list
        else:
            moves_list = self.__get_moves_list(side)

        if moves_list and current_prediction_depth < MAX_PREDICTION_DEPTH:
            board_copy = Board.copy(self.__board)
            for move in moves_list:
                has_killed_piece = self.__handle_move(move, draw=False)

                required_moves_list = list(
                    filter(
                        lambda required_move: move.to_x == required_move.from_x
                        and move.to_y == required_move.from_y,
                        self.__get_required_moves_list(side),
                    )
                )

                # check if the current piece can move again
                if has_killed_piece and required_moves_list:
                    self.__get_predicted_moves_list(
                        side,
                        current_prediction_depth,
                        all_moves_list,
                        current_moves_list + [move],
                        required_moves_list,
                    )
                else:
                    self.__get_predicted_moves_list(
                        SideType.opposite(side),
                        current_prediction_depth + 1,
                        all_moves_list,
                        current_moves_list + [move],
                    )

                self.__board = Board.copy(board_copy)

        return all_moves_list

    def __get_moves_list(self, side: SideType) -> list[Move]:
        """Get the list of moves for the specified side.

        Args:
            side (SideType): The side for which to get the moves.

        Returns:
            list[Move]: The list of moves for the specified side.
        """
        moves_list = self.__get_required_moves_list(side)
        if not (moves_list):
            moves_list = self.__get_optional_moves_list(side)
        return moves_list

    def __get_required_moves_list(self, side: SideType) -> list[Move]:
        """Get the list of mandatory moves.

        Args:
            side (SideType): The side for which to get the mandatory moves.

        Returns:
            list[Move]: The list of mandatory moves.
        """
        moves_list = []

        if side == SideType.WHITE:
            friendly_pieces = WHITE_PIECES
            enemy_pieces = BLACK_PIECES
        elif side == SideType.BLACK:
            friendly_pieces = BLACK_PIECES
            enemy_pieces = WHITE_PIECES
        else:
            return moves_list

        for y in range(self.__board.y_size):
            for x in range(self.__board.x_size):
                if self.__board.type_at(x, y) == friendly_pieces[0]:
                    for offset in MOVE_OFFSETS:
                        if not (
                            self.__board.is_within(x + offset.x * 2, y + offset.y * 2)
                        ):
                            continue

                        # check if the enemy piece is in front and an empty space is two steps ahead
                        if (
                            self.__board.type_at(x + offset.x, y + offset.y)
                            in enemy_pieces
                            and self.__board.type_at(x + offset.x * 2, y + offset.y * 2)
                            == PieceType.NONE
                            and (
                                offset.y < 0 if side == SideType.WHITE else offset.y > 0
                            )
                        ):
                            moves_list.append(
                                Move(x, y, x + offset.x * 2, y + offset.y * 2)
                            )

        return moves_list

    def __get_optional_moves_list(self, side: SideType) -> list[Move]:
        """Get the list of optional moves for a given side.

        Args:
            side (SideType): The side for which to get the optional moves.

        Returns:
            list[Move]: The list of optional moves.

        """
        moves_list = []

        if side == SideType.WHITE:
            friendly_pieces = WHITE_PIECES
        elif side == SideType.BLACK:
            friendly_pieces = BLACK_PIECES
        else:
            return moves_list

        for y in range(self.__board.y_size):
            for x in range(self.__board.x_size):
                if self.__board.type_at(x, y) == friendly_pieces[0]:
                    for offset in (
                        MOVE_OFFSETS[:2] if side == SideType.WHITE else MOVE_OFFSETS[2:]
                    ):
                        if not (self.__board.is_within(x + offset.x, y + offset.y)):
                            continue

                        if (
                            self.__board.type_at(x + offset.x, y + offset.y)
                            == PieceType.NONE
                        ):
                            moves_list.append(Move(x, y, x + offset.x, y + offset.y))

        return moves_list

    def get_flattened_state(self) -> List[int]:
        """Get the flattened representation of the current game state.

        Returns:
            List[int]: A list of integers representing the piece types in the game state.
        """
        state = []
        for y in range(self.__board.y_size):
            for x in range(self.__board.x_size):
                piece_type = self.__board.type_at(x, y).value
                state.append(piece_type)
        return state
