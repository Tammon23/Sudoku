from colorama import Fore, Style
import subprocess
import random
import sys

# gBoard = [
#         [0, 0, 0, 0, 0, 8, 3, 0, 7],
#         [0, 5, 8, 0, 0, 0, 0, 2, 0],
#         [0, 0, 0, 1, 2, 6, 8, 0, 4],
#         [0, 0, 0, 3, 7, 9, 6, 0, 5],
#         [0, 8, 0, 4, 0, 2, 0, 3, 0],
#         [3, 0, 7, 8, 5, 1, 0, 0, 0],
#         [2, 0, 1, 7, 8, 3, 0, 0, 0],
#         [0, 3, 0, 0, 0, 0, 2, 1, 0],
#         [8, 0, 6, 2, 0, 0, 0, 0, 0]
#         ]


# used to display the gameboard to the terminal, as well as an optional output message
def display(gameBoard, message=None):
    if message != None:
        print(message)

    rowLength = len(gameBoard)
    colLength = len(gameBoard[0])

    for row in range(rowLength):
        for col in range(colLength):
            v = gameBoard[row][col]
            # if v != 0:
            #     print(f"{Fore.RED}"+str(v)+"{Style.RESET_ALL} ", end = "")
            # else:
            #     print(str(v) + " ", end = "")
            print(str(v) + " ", end = "")

            if col % 3 == 2 and col != colLength - 1:
                print("║ " , end="")

        print("")
        if row % 3 == 2 and row != rowLength - 1:
            print("╟═══════════════════╢")

def terminal_clear():
    subprocess.run(["clear"])

def locateEmpty(board):
    for r, row in enumerate(board):
        for c, cell in enumerate(row):
            if cell == 0:
                return (r,c)
    return (None, None)

# validates that row that a given input is in is valid
def validRow(board, row, value):
    tRow = board[row]
    if value in tRow:
        return False
    return True


# validates that column that a given input is in is valid
def validCol(board, col, value):
    tCol = []
    for i in range(len(board[0])):
        tCol.append(board[i][col])

    if value in tCol:
        return False
    return True

# validates that block that a given input is in is valid
def validSection(board, row, col, value):
    tSec = []
    row = row - row % 3
    col = col - col % 3
    for i in range(3):
        for j in range(3):
            tSec.append(board[i+row][j+col])

    if value in tSec:
        return False
    return True

def validMove(board, row, col, i):
    if validRow(board, row, i) and validCol(board, col, i) and validSection(board, row, col, i):
        return True
    return False

def validBoard(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return False

            t = board[i][j]
            board[i][j] = 0
            if not validMove(board, i, j, t):
                return False
            board[i][j] = t
    return True

def validRange(c):
    return (c >= 0 and c <= 9)

# the actual function that will solve the sudoku
def backTrack(board):
    row, col = locateEmpty(board)

    if row is None:
        return board

    for i in range (1, 10):
        if validMove(board, row, col, i):
            board[row][col] = i

            if type(backTrack(board)) == list:
                return board

            board[row][col] = 0

    return False

def generateBoard(mode):
    """
    code found at https://stackoverflow.com/questions/45471152/how-to-create-a-sudoku-puzzle-in-python
    written by https://stackoverflow.com/users/5237560/alain-t
    """
    arr = [ [ 0 for i in range(9) ] for j in range(9) ]
    base  = 3
    side  = base*base

    def pattern(r,c):
        return (base*(r%base)+r//base+c)%side
    # pattern for a baseline valid solution
    def shuffle(s):
        return random.sample(s,len(s))

    rBase = range(base)
    rows  = [ g*base + r for g in shuffle(rBase) for r in shuffle(rBase) ]
    cols  = [ g*base + c for g in shuffle(rBase) for c in shuffle(rBase) ]
    nums  = shuffle(range(1,base*base+1))

    # produce board using randomized baseline pattern
    arr = [ [nums[pattern(r,c)] for c in cols] for r in rows ]

    #display(arr, "This should be the finished board")
    # at this point we should have a finished board
    # assigning a range of numbers to remove based on mode
    if mode == 0:
        lower = 30
        upper = 40

    elif mode == 1:
        lower = 27
        upper = 35

    elif mode == 2:
        lower = 20
        upper = 27

    # determining how many numbers to remove, then removing that many numbers
    removeNum = 81 - random.randint(lower, upper)
    pCells = []
    for x in range(9):
        for y in range(9):
            pCells.append((x,y))

    random.shuffle(pCells)
    for x in range(removeNum):
        row, col = pCells.pop()
        arr[row][col] = 0 # erasing that digit

    #display(arr, "This should be the board that the user is playing")
    return arr

def makeMove(b, row, col):
    if b[row][col] != 0:
        return False
    else:
        while(True):
            try:
                v = int(input("What value you want to input? "))
                if not validRange(v):
                    terminal_clear()
                    display(b)
                    print("Invalid range!")
                    continue
                else:
                    b[row][col] = v
                    terminal_clear()
                    display(b)
                    return True

            except ValueError:
                terminal_clear()
                display(b)
                print("number between 0 - 9 only!")


def isFullBoard(b):
    x, y = locateEmpty(b)
    if x == None:
        return True
    return False

def terminalSudoku(mode=0):
    terminal_clear()
    """
    3 possible modes, depending on the mode is the amount of given blocks
    0 = easy | 30 - 40
    1 = medium | 27 - 35
    2 = hard | 25 - 30
    """
    b = generateBoard(mode)
    display(b)
    obtainingLocation = True
    while(obtainingLocation):
        loc = input("Cell #\nForm ->\nrow col (0 indexing): ")
        loc = loc.split()
        if len(loc) != 2:
            terminal_clear()
            display(b)
            print("Invalid input try again.")
        else:
            try:
                loc[0], loc[1] = int(loc[0]), int(loc[1])
                if not validRange(loc[0]) and not validRange(loc[1]):
                    print("Pleae provide a valid range number")
                elif(not makeMove(b, loc[0], loc[1])):
                    terminal_clear()
                    display(b)
                    print("Cell is not empty. Choose again!")

            except ValueError:
                terminal_clear()
                display(b)
                print("Please enter only integers")

        if isFullBoard(b):
            while(True):
                try:
                    choice = input("Would you like to check game result? y/N").lower()
                    if choice == "y":
                        if(validBoard(b)):
                            print("GG you win")
                        else:
                            print("Sorry, you made a mistake somewhere")
                        return
                    elif choice == "n":
                        pass
                    else:
                        print("y/N are only valid options")

                except ValueError:
                    print("y/N are only valid options")

def turtleSudoku(mode=0):
    pass

#TODO s
# possible problem can't undo choices
# make constants red nad other numbers default
# implement turtle cersion
# choice in terminal command line
#main():

def main():
    mode = diff = 0 # 0 is default argument

    try:
        mode = sys.argv[1]
        diff = sys.argv[2]
    except IndexError:
        pass

    if mode == 0:
        print("Mode is: {}, Difficulty Level: {}".format(mode, diff))
        terminalSudoku(diff)
    else:
        turtleSudoku(diff)

if __name__ == "__main__":
    main()

picces = "║ │ ╟ ╠ ─ ╣ ╢ ╝ ╚ ═  ╔ ╦ ╤ ╗"