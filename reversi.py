"""

"""

from board import Board
from tkinter import *
import random

def main():
    reversi = Board(8, 8)
    reversi.setColor(input("1 - White\n2 - Black\nChoose your color: "))
    reversi.setFirstPlayer(str(random.randint(1,2)))
    print("Welcome to Reversi:")

    playerMove = []
    comMove = []
    boardWithMoves = []
    comTile = reversi.otherTile(reversi.tile)
    print("Player:", reversi.tile, reversi.TILE[reversi.tile])
    print("Computer:", comTile, reversi.TILE[comTile])
    turn = reversi.first
    while True:
        while True:
            # Player turn
            if reversi.end[0] and reversi.end[1]:
                break
            elif turn == reversi.STATUS[0]:
                # Display a board with all possible moves
                boardWithMoves = reversi.getBoardWithValidMoves(reversi.tile)
                reversi.printBoard(boardWithMoves)
                reversi.showScore()
                # Player have to pass his turn
                if reversi.board == boardWithMoves:
                    input("You can't make any move. Press Enter to continue.")
                    reversi.end[0] = True
                # Player plays a move
                else:
                    reversi.end[0] = False
                    playerMove = reversi.playerMove(input("Enter your move, or press ENTER to end the game: "))
                    # Quit the game
                    if playerMove == reversi.STATUS[2]:
                        print('Thank you for playing.')
                        sys.exit() # terminate the program
                    # Flip tiles captured by the player
                    else:
                        reversi.flip(reversi.board, reversi.tile, playerMove[0], playerMove[1], reversi.flipThis)
                # Set the turn for the computer
                turn = reversi.STATUS[1]
            # Computer's turn.
            else:
                print("Computer turn.")
                boardWithMoves = reversi.getBoardWithValidMoves(reversi.tile)
                reversi.printBoard(reversi.board)
                reversi.showScore()
                if reversi.board == boardWithMoves:
                    input("Computer can't make any move. Press Enter to continue.")
                    reversi.end[1] = True
                else:
                    reversi.end[1] = False
                    input("Press Enter to continue.")
                    comMove = reversi.getComputerMove(reversi.board, comTile)
                    reversi.flip(reversi.board, comTile, comMove[0], comMove[1], reversi.validMove(reversi.board, comTile, comMove[0], comMove[1]))
                    # Set the turn for the player
                turn = reversi.STATUS[0]
        # Prompt the user if he wants to play again
        reversi.getFinalScore()
        if not reversi.playAgain():
            break
        else:
            reversi.end[0] = False
            reversi.end[1] = False


main()