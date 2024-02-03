from tkinter import Tk, Canvas, PhotoImage
from checkers.game import Game
from checkers.constants import X_SIZE, Y_SIZE, CELL_SIZE


def main():
    # main window
    main_window = Tk()
    main_window.title("American Checkers")
    main_window.resizable(0, 0)
    main_window.iconphoto(False, PhotoImage(file="./assets/icon.png"))

    # create canvas
    main_canvas = Canvas(
        main_window, width=CELL_SIZE * X_SIZE, height=CELL_SIZE * Y_SIZE
    )
    main_canvas.pack()

    game = Game(main_canvas, X_SIZE, Y_SIZE)

    main_canvas.bind("<Motion>", game.mouse_move)
    main_canvas.bind("<Button-1>", game.mouse_down)

    main_window.mainloop()


if __name__ == "__main__":
    main()
