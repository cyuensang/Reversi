"""

"""
from board import Board
from gui_board import GuiBoard
from tkinter import *


BOARD_WIDTH = 55 * 8
BOARD_HEIGHT = 55 * 8
WINDOW_WIDTH = 650
WINDOW_HEIGHT = 500


def main():
    root = Tk()
    reversi = Board(8, 8)
    reversiGui = GuiBoard(root, reversi)
    board = reversi.getBoard()

    # get screen width and height
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # calculate x and y coordinates for the Tk root window
    x = (ws / 2) - (WINDOW_WIDTH / 2)
    y = (hs / 2) - (WINDOW_HEIGHT / 2)
    # set the dimensions of the screen and where it is placed
    root.geometry('%dx%d+%d+%d' % (WINDOW_WIDTH, WINDOW_HEIGHT, x, y))
    column_width = BOARD_WIDTH / reversi.columns
    row_height = BOARD_HEIGHT / reversi.rows
    root.wm_title("Reversi")

    #reversiGui.diplayBoard(reversi.getBoard())
    reversiGui.diplayBoard(reversi.getBoardWithValidMoves(reversi.tile))

    '''
    choose = Toplevel()
    ws = choose.winfo_screenwidth()
    hs = choose.winfo_screenheight()
    # calculate x and y coordinates for the Tk root window
    x = (ws / 2) - (100 / 2)
    y = (hs / 2) - (100 / 2)
    # set the dimensions of the screen and where it is placed
    choose.geometry('%dx%d+%d+%d' % (100, 100, x, y))
    choose.title = "Color"
    Label(choose, text = "Choose your color:").pack()

    def white():
        reversi.tile = "white"
        reversiGui.diplayBoard(reversi.getBoardWithValidMoves(reversi.tile))
        #choose.destroy()
    Button(choose, text = "White", command = white()).pack()

    def black():
        reversi.tile = "black"
        reversiGui.diplayBoard(reversi.getBoardWithValidMoves(reversi.tile))
        #choose.destroy()
    Button(choose, text = "Black", command = black()).pack()
    '''


    if reversiGui.turn == "HUM":
        reversiGui.updateText("\n---- Player's turn")
        reversiGui.display.bind('<ButtonPress -1>', reversiGui.getMove)
    else:
        # Computer turn
        reversiGui.comPlay()
        reversiGui.display.bind('<ButtonPress -1>', reversiGui.getMove)


    root.mainloop()


main()