"""

"""

from board import Board
from tkinter import *
from tkinter import messagebox

import random

class GuiBoard:

    BOARD_WIDTH = 55 * 8
    BOARD_HEIGHT = 55 * 8
    WINDOW_WIDTH = 650
    WINDOW_HEIGHT = 500

    def __init__(self, root, game):
        # Gui variable
        self.game = game
        self.column_width = self.BOARD_WIDTH / self.game.columns
        self.row_height = self.BOARD_HEIGHT / self.game.rows
        self.scoreTab = []

        # Canvas
        self.display = Canvas(root, bg = "white", width = self.BOARD_WIDTH, height = self.BOARD_HEIGHT)
        self.display.grid(row = 1, column = 1)

        # Message
        scroll = Scrollbar(root)
        self.textField = Text(root, width = 23, height = 32)

        self.textField.grid(row = 1, column = 2)
        scroll.grid(row = 1, column = 3, sticky = 'ns', rowspan = 1)

        self.textField.config(state = DISABLED)# text in read only
        scroll.config(command = self.textField.yview)
        self.textField.config(yscrollcommand = scroll.set)
        self.updateText("Welcome!")

        # n# horizontal
        horizontal = Canvas(root, width = self.BOARD_WIDTH, height = 20)
        y = 13
        for digit in range(1,9):
            x = (digit - 1) * (self.column_width / 2) + \
                ((digit - 1) * (self.column_width / 2)) + self.column_width / 2
            horizontal.create_text(x, y, font=("Times", 16), text= str(digit))

        horizontal.grid(row = 0, column = 1)

        # n# vertical
        vertical = Canvas(root, width = 20, height = self.BOARD_HEIGHT)
        x = 13
        for digit in range(1,9):
            y = (digit - 1) * (self.row_height / 2) + \
                    ((digit - 1) * (self.row_height / 2)) + self.row_height / 2
            vertical.create_text(x, y, font=("Times", 16), text= str(digit))

        vertical.grid(row = 1, column = 0)

        # Scores:
        self.scoreVar = StringVar()
        self.updateScores()
        self.scores = Message(root, textvariable = self.scoreVar, font=("Times", 16), width = 250)
        self.scores.grid(row = 2, column = 1)

        # Game variable
        self.playerMove = []
        self.comMove = []

        if random.randint(0, 1) == 0:
            self.turn = "HUM"
        else:
            self.turn = "COM"


    def diplayBoard(self, board):
        self.display.delete(ALL)
        for y in range(self.game.rows):
            for x in range(self.game.columns):
                x1 = x * self.column_width
                y1 = y * self.row_height
                x2 = x1 + self.column_width
                y2 = y1 + self.row_height
                self.display.create_rectangle(x1, y1, x2, y2, fill = "gray")
                if board[x][y] == '.':
                    self.display.create_oval(x1, y1, x2, y2)
                if board[x][y] == self.game.TILE["white"]:
                    self.display.create_oval(x1, y1, x2, y2, fill = "white", outline = "black")
                if board[x][y] == self.game.TILE["black"]:
                    self.display.create_oval(x1, y1, x2, y2, fill = "black", outline = "white")
        self.display.update()


    def getMove(self, event):
        self.playerMove = [int(event.x // self.column_width), int(event.y // self.row_height)]
        self.playerTurn()
        return



    def playerTurn(self):
        if not self.cantMove("HUM"):
            self.updateText("\nPlayer's move: [" + str(self.playerMove[0] + 1) + ", " + str(self.playerMove[1] + 1) + "]")
            self.textField.see(END)
            if self.game.validMove(self.game.board, self.game.tile, self.playerMove[0], self.playerMove[1]) != False:
                self.game.flip(self.game.board, self.game.tile, self.playerMove[0], self.playerMove[1],
                               self.game.validMove(self.game.board, self.game.tile, self.playerMove[0], self.playerMove[1]))
                self.updateScores()
                if not self.gameEnd():
                    self.display.after(300, self.comPlay())
            else:
                self.updateText("\nInvalid move.")
                self.textField.see(END)
            self.playerMove = []
        else:
            self.updateText("\nPlayer can't make any move.")
            self.textField.see(END)
            if not self.gameEnd():
                self.display.after(300, self.comPlay())


    def comPlay(self):
        # Computer turn
        self.updateText("\n---- Computer's turn")
        self.textField.see(END)
        if not self.cantMove("COM"):
            self.computerTurn()
            self.updateScores()
            self.display.after(300, lambda: self.diplayBoard(self.game.getBoardWithValidMoves(self.game.tile)))
            self.playerNextTurn()
        else:
            self.updateText("\nComputer can't make any move.")
            self.textField.see(END)
            self.playerNextTurn()


    def computerTurn(self):
        comTile = self.game.otherTile(self.game.tile)
        self.comMove = self.game.getComputerMove(self.game.board, comTile)
        if self.comMove:
            self.updateText("\nComputer's move: [" + str(self.comMove[0] + 1) + ", " + str(self.comMove[1] + 1) + "]")
            self.textField.see(END)
            self.game.flip(self.game.board, comTile, self.comMove[0], self.comMove[1],
                        self.game.validMove(self.game.board, comTile, self.comMove[0], self.comMove[1]))
        else:
            self.updateText("\nComputer can't make any move.")
            self.textField.see(END)


    def cantMove(self, player):
        if player == "HUM":
            tile = self.game.tile
        else:
            tile = self.game.otherTile((self.game.tile))
        allMoves = self.game.getAllValidMoves(self.game.board, tile)
        if not allMoves:
            return True
        return False


    def playerNextTurn(self):
        if not self.gameEnd():
                if not self.cantMove("HUM"):
                    self.updateText("\n---- Player's turn")
                    self.textField.see(END)
                    self.diplayBoard(self.game.getBoardWithValidMoves(self.game.tile))
                else:
                    self.updateText("\nPlayer can't make any move.")
                    self.textField.see(END)
                    self.comPlay()


    def gameEnd(self):
        self.display.after(300, self.diplayBoard(self.game.board))
        if self.cantMove("HUM") and self.cantMove("COM"):
            self.updateText("\n---- Game end.")
            self.textField.see(END)
            messagebox.showinfo("Final Scores", self.getFinalScore())
            self.display.after(500, lambda: sys.exit())
            return True
        else:
            return False

    def updateText(self, text):
        self.textField.config(state = NORMAL)
        self.textField.insert(END, text)
        self.textField.config(state = DISABLED)


    def updateScores(self):
        scores = self.game.getScore(self.game.board)
        player = self.game.tile
        computer = self.game.otherTile(self.game.tile)
        self.scoreVar.set("Player : " + str(scores[player]) + " - Computer : " + str(scores[computer]))


    def getFinalScore(self):
        """ Get the final score """
        finalScores = ""
        scores = self.game.getScore(self.game.board)
        player = self.game.tile
        computer = self.game.otherTile(self.game.tile)
        if scores[player] > scores[computer]:
            finalScores = "You beat the computer by %s points." % (scores[player] - scores[computer])
        elif scores[player] < scores[computer]:
            finalScores = "You lost. The computer beat you by %s points." % (scores[computer] - scores[player])
        else:
            finalScores = "The game was a tie."
        return finalScores