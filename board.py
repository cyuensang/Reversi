"""

"""
import sys

class Board:

    TILE = {"white": 'O', "black": 'X'}
    COLOR = ("white", "black")
    STATUS = ("HUM", "COM", "QUIT")
    # Down, DownRight, Right, UpRight, Up, UpLeft, Left, UpLeft
    MOVES = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]

    def __init__(self ,rows, columns, tile = "white", first = "HUM"):
        """ Initialise a Reversi board """
        self.rows = rows
        self.columns = columns
        self.tile = tile
        self.first = first
        # contain a list of positions of tiles to flip or false if there are none
        self.flipThis = []
        self.end = [False, False]
        self.initialise()
        self.comBestMove = []

    def __str__(self):
        """ Print the board """
        HLINE = '  +---+---+---+---+---+---+---+---+'

        print('    1   2   3   4   5   6   7   8')
        print(HLINE)
        for y in range(self.columns):
            print(y+1, end=' ')
            for x in range(self.rows):
                print('| %s' % (self.board[x][y]), end=' ')
            print('|')
            print(HLINE)

    def initialise(self):
        """ Reset the board """
        self.board = self.getNewBoard()
        self.board[3][3] = self.TILE["black"]
        self.board[3][4] = self.TILE["white"]
        self.board[4][4] = self.TILE["black"]
        self.board[4][3] = self.TILE["white"]

    def getTile(self):
        """ Return player color """
        return self.tile

    def getBoard(self):
        """ Return a copy of the board """
        copy = self.getNewBoard()
        for y in range(self.rows):
            for x in range(self.columns):
                copy[x][y] = self.board[x][y]
        return copy

    def getFirst(self):
        """ Return who play first """
        return self.first

    def getAllValidMoves(self, board, tile):
        """ Returns a list of coordinates for all valid moves for the given tile and board """
        moves = []
        for y in range(self.rows):
            for x in range(self.columns):
                if self.validMove(board, tile, x, y) != False:
                    moves.append([x, y])
        return moves

    def setColor(self, choice):
        """ Only '1' and '2' are valid inputs to set the player color """
        while choice not in ('1', '2') or not choice:
            choice = input()
        self.tile = self.COLOR[int(choice) - 1]

    def setFirstPlayer(self, choice):
        """ Only '1' and '2' are valid input to set who play first """
        while choice not in ('1', '2') or not choice:
            choice = input()
        self.first = self.STATUS[int(choice) - 1]

    def play(self):
        playerMove = []
        comMove = []
        boardWithMoves = []
        comTile = self.otherTile(self.tile)
        print("Player:", self.tile, self.TILE[self.tile])
        print("Computer:", comTile, self.TILE[comTile])
        turn = self.first
        while True:
            while True:
                # Player turn
                if self.end[0] and self.end[1] and self.remainingTile() <= 0:
                    break
                elif turn == self.STATUS[0]:
                    # Display a board with all possible moves
                    boardWithMoves = self.getBoardWithValidMoves(self.tile)
                    self.printBoard(boardWithMoves)
                    self.showScore()
                    # Player have to pass his turn
                    if self.board == boardWithMoves:
                        input("You can't make any move. Press Enter to continue.")
                        self.self.end[0] = True
                    # Player plays a move
                    else:
                        self.end[0] = False
                        playerMove = self.playerMove(input("Enter your move, or press ENTER to end the game: "))
                        # Quit the game
                        if playerMove == self.STATUS[2]:
                            print('Thank you for playing.')
                            sys.exit() # terminate the program
                        # Flip tiles captured by the player
                        else:
                            self.flip(self.board, self.tile, playerMove[0], playerMove[1], self.flipThis)
                    # Set the turn for the computer
                    turn = self.STATUS[1]
                # Computer's turn.
                else:
                    print("Computer turn.")
                    boardWithMoves = self.getBoardWithValidMoves(self.tile)
                    self.printBoard(self.board)
                    self.showScore()
                    if self.board == boardWithMoves:
                        input("Computer can't make any move. Press Enter to continue.")
                        self.end[1] = True
                    else:
                        self.end[1] = False
                        input("Press Enter to continue.")
                        comMove = self.getComputerMove(self.board, comTile)
                        self.flip(self.board, comTile, comMove[0], comMove[1], self.validMove(self.board, comTile, comMove[0], comMove[1]))
                        # Set the turn for the player
                    turn = self.STATUS[0]
            # Prompt the user if he wants to play again
            self.getFinalScore()
            if not self.playAgain():
                break
            else:
                self.end[0] = False
                self.end[1] = False

    #------------------------------------------------------------------------------

    def getNewBoard(self):
        # Creates a brand new, blank board data structure.
        board = []
        for y in range(self.rows):
            board.append([' '] * self.columns)

        return board

    def onBoard(self, x, y):
        """ Returns True if the coordinates are located on the board. """
        return (x >= 0 and x < self.columns) and (y >= 0 and y < self.rows)

    def otherTile(self, tile):
        """ Return the other side of the tile """
        if tile == self.COLOR[0]:
            return self.COLOR[1]
        else:
            return self.COLOR[0]


    def validMove(self, board, tile, xstart, ystart):
        """ Check if it is valid move for the given player and board """
        flipThis = [] # list of all tile to flip
        other = self.otherTile(tile)
        # A move outside of the board or in an occupied space
        if board[xstart][ystart] != " " or not self.onBoard(xstart, ystart):
            return False
        # Check if the move is valid in all eight directions
        for xdir, ydir in self.MOVES:
            x = xstart + xdir
            y = ystart + ydir
            # If an opposite tile is found continue
            if self.onBoard(x, y) and board[x][y] == self.TILE[other]:
                x += xdir
                y += ydir
                # Continue to navigate in that direction as long as an opposite tile is found
                while self.onBoard(x, y) and board[x][y] == self.TILE[other]:
                    x += xdir
                    y += ydir
                # A tile of the current player have been found
                if self.onBoard(x, y) and board[x][y] == self.TILE[tile]:
                    # Do the process in reverse to store the positon of all tile to flip
                    while True:
                        x -= xdir
                        y -= ydir
                        # Finish the process when we reach the initial position
                        if x == xstart and y == ystart:
                            break
                        # Store all position of tiles to flip
                        flipThis.append([x, y])
        # The list is empty, no valid moves have been found
        if len(flipThis) == 0:
            return False
        # Valid moves have been found, return the position of tiles to flip
        return flipThis

    def getBoardWithValidMoves(self, tile):
        """ Returns a new board with all possible moves marked for the given tile. """
        boardWithMoves = self.getBoard()
        for x, y in self.getAllValidMoves(self.board, tile):
            boardWithMoves[x][y] = '.'
        return boardWithMoves

    def playerMove(self, move):
        """ Player turn to make a move"""
        digits = '1 2 3 4 5 6 7 8'.split()
        while True:
            # Exit the game
            if not move:
                return self.STATUS[2]
                break
            print("Move to check:", move)
            if len(move) == 2 and move[0] in digits and move[1] in digits:
                x = int(move[0]) - 1
                y = int(move[1]) - 1
                self.flipThis = self.validMove(self.board, self.tile, x, y)
                if self.flipThis == False:
                    print("Invalid move.")
                else:
                    break
            print("Done checking move")
        return [x, y]

    def getComputerMove(self, board, comTile):
        """ Computer move: It will determine what is the best current move from all possible moves"""
        possibleMoves = self.getAllValidMoves(board, comTile)
        bestScore = -1
        bestMove = []
        # Put the tile in a corner
        for x, y in possibleMoves:
            if (x == 0 and y == 0) or (x == self.columns - 1 and y == 0) \
                    or (x == 0 and y == self.rows - 1) or (x == self.columns - 1 and y == self.rows - 1):
                return [x, y]
        # Go through all the possible moves and remember the best scoring move
        for x, y in possibleMoves:
            testBoard = self.getBoard()
            self.flip(testBoard, comTile, x, y, self.validMove(board, comTile, x, y))
            score = self.getScore(testBoard)[comTile]
            if score > bestScore:
                bestMove = [x, y]
                bestScore = score
        if bestMove:
            self.comBestMove = bestMove
            return bestMove
        else:
            self.comBestMove = []
            return False

    def printBoard(self, board):
        """ Print the given board """
        HLINE = '  +---+---+---+---+---+---+---+---+'

        print('    1   2   3   4   5   6   7   8')
        print(HLINE)
        for y in range(self.rows):
            print(y+1, end=' ')
            for x in range(self.columns):
                print('| %s' % (board[x][y]), end=' ')
            print('|')
            print(HLINE)

    def flip(self, board, tile, posX, posY, flipThis):
        """ Flip all tiles from the flipThis list """
        board[posX][posY] = self.TILE[tile]
        if flipThis != False:
            for x, y in flipThis:
                board[x][y] = self.TILE[tile]

    def getScore(self, board):
        """ Process the score by counting tiles of each players from the given board. """
        white = 0
        black = 0
        for y in range(self.rows):
            for x in range(self.columns):
                if board[x][y] == self.TILE["white"]:
                    white += 1
                if board[x][y] == self.TILE["black"]:
                    black += 1
        return {"white": white, "black": black}

    def showScore(self):
        """ Display the current score """
        scores = self.getScore(self.board)
        player = self.tile
        computer = self.otherTile(self.tile)
        print("Score: Player " + str(scores[player]) + " - Computer " + str(scores[computer]))

    def getFinalScore(self):
        """ Display the final score """
        self.printBoard(self.board)
        scores = self.getScore(self.board)
        player = self.tile
        computer = self.otherTile(self.tile)
        print("Score: Player " + str(scores[player]) + " - Computer " + str(scores[computer]))
        if scores[player] > scores[computer]:
            print("You beat the computer by %s points: " % (scores[player] - scores[computer]))
        elif scores[player] < scores[computer]:
            print("You lost. The computer beat you by %s points." % (scores[computer] - scores[player]))
        else:
            print("The game was a tie.")

    def playAgain(self):
        """ Prompt the player if he wants to play again """
        print('Do you want to play again? (yes or no)')
        return input().lower().startswith('y')
