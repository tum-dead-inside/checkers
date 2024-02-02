import tkinter as tk
import checkers_rules as rules


class CheckersGame:
    def __init__(self):
        self.board = [
            ["B", " ", "B", " ", "B", " "],
            [" ", "B", " ", "B", " ", "B"],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", "W", " ", "W", " ", "W"],
            ["W", " ", "W", " ", "W", " "],
        ]
        self.rules = rules.CheckersRules(self.board)

        self.window = tk.Tk()
        self.window.title("American Checkers")

        self.canvas = tk.Canvas(self.window)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.window.bind("<Configure>", self.on_window_resize)
        self.draw_board()

        self.current_player = "W"  # start with player w

        # bind mouse click event to handle player's move
        self.canvas.bind("<Button-1>", self.on_mouse_click)

    def on_window_resize(self, event):
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        cell_size = min(width, height) // 6

        board_width = cell_size * 6
        board_height = cell_size * 6

        x_offset = (width - board_width) // 2
        y_offset = (height - board_height) // 2

        for row in range(6):
            for col in range(6):
                x1 = x_offset + col * cell_size
                y1 = y_offset + row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                if (row + col) % 2 == 0:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#393939")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#161616")

                pieces_size = cell_size // 4
                if self.board[row][col] == "W":
                    self.canvas.create_oval(
                        x1 + pieces_size,
                        y1 + pieces_size,
                        x2 - pieces_size,
                        y2 - pieces_size,
                        fill="#fff",
                    )
                elif self.board[row][col] == "B":
                    self.canvas.create_oval(
                        x1 + pieces_size,
                        y1 + pieces_size,
                        x2 - pieces_size,
                        y2 - pieces_size,
                        fill="#be95ff",
                    )

    def run(self):
        self.window.update_idletasks()
        board_width = self.canvas.winfo_reqwidth()
        board_height = self.canvas.winfo_reqheight()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_width = min(board_width * 4, screen_width) - 460
        window_height = min(board_height * 4, screen_height)
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.window.mainloop()

    def on_mouse_click(self, event):
        # get the clicked cell coordinates
        cell_size = min(self.canvas.winfo_width(), self.canvas.winfo_height()) // 6
        col = (event.x - (event.x % cell_size)) // cell_size
        row = (event.y - (event.y % cell_size)) // cell_size

        # make sure the clicked cell is within the board
        if 0 <= row < 6 and 0 <= col < 6:
            # check if it's the current player's turn
            if self.board[row][col] == self.current_player:
                # handle the player's move
                self.handle_move(row, col)

    def handle_move(self, row, col):
        # check what moves are available
        if self.current_player == "W":
            moves = self.rules.get_valid_moves("W", row, col)
        else:
            moves = self.rules.get_valid_moves("B", row, col)

        cell_size = min(self.canvas.winfo_width(), self.canvas.winfo_height()) // 6

        # draw a rectangle around the squares that can be moved to
        for move in moves:
            x1 = move[1] * cell_size
            y1 = move[0] * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="#00ff00", width=3)

        # TODO: fix bug where the player decides to change their mind and click on a different piece

        # wait until the player clicks on one of the valid moves
        self.canvas.bind(
            "<Button-1>",
            lambda event: self.on_move_click(event, moves, row, col),
        )

    def on_move_click(self, event, moves, old_row, old_col):
        cell_size = min(self.canvas.winfo_width(), self.canvas.winfo_height()) // 6
        col = (event.x - (event.x % cell_size)) // cell_size
        row = (event.y - (event.y % cell_size)) // cell_size

        if (row, col) in moves:
            self.board[row][col] = self.current_player
            self.board[old_row][old_col] = " "
            self.draw_board()

        # unbind the click event
        self.canvas.bind("<Button-1>", self.on_mouse_click)

        # update the current player
        self.current_player = "W" if self.current_player == "B" else "B"
        self.draw_board()


game = CheckersGame()
game.run()
