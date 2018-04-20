from random import randrange
from matrix_expansion import findSurroundings

class Board:

    def __init__(self, size, n_bombs):
        self.size = size
        self.n_bombs = n_bombs

        self.board = []
        for n in range(size):
            self.board.append(["+" for i in range(size)])

    def printBoard(self, finish=False):
        print("\n    ", end="")
        for n in range(self.size):
            if n < 9:
                print(n, end="  ")
            else:
                print(n, end=" ")
        print()

        for i in range(self.size):
            if i < 10:
                print(i, end="  ")
            else:
                print(i, end=" ")
                
            for j in range(self.size):
                if self.board[i][j] == "B":
                    if finish:
                        print("[B]", end="")
                    else:
                        print("[+]", end="")
                else:
                    print("[" + self.board[i][j] + "]", end="")

            if i < 10:
                print(" ", i)
            else:
                print("", i)
            
        print("    ", end="")
        for n in range(self.size):
            if n < 9:
                print(n, end="  ")
            else:
                print(n, end=" ")
        print("\n")

    def _setPosition(self, pos, val):
        self.board[pos[0]][pos[1]] = val

    def setBombs(self, first):
        bombs = []

        for b in range(self.n_bombs):
            while True:
                posi = randrange(self.size)
                posj = randrange(self.size)
                surr_first = findSurroundings(self.board, first)
                if [posi, posj] != first and [posi, posj] not in bombs\
                   and [posi, posj] not in surr_first:
                    break
            bombs.append([posi, posj])

        for pos in bombs:
            self._setPosition(pos, "B")

    def isBomb(self, p):
        return self.board[p[0]][p[1]] == "B"

    def isNeutral(self, p):
        return self.board[p[0]][p[1]] == " "

    def isNumber(self, p):
        return self.board[p[0]][p[1]].isdigit()

    def _countBombs(self, p):
        surr_p = findSurroundings(self.board, p)
        n_bombs = 0
        for pos in surr_p:
            if self.isBomb(pos):
                n_bombs += 1

        return n_bombs

    def expandPosition(self, p):
        #already supposes that the initial position is neither a
        #bomb nor a neutralized square nor a numerated square

        checking = [p]

        to_check = []

        while checking != []:

            for pos in checking:
                if self.isBomb(pos) or self.isNeutral(pos) or self.isNumber(pos):
                    continue

                n_bombs = self._countBombs(pos)
                if n_bombs > 0:
                    self._setPosition(pos, str(n_bombs))
                else: #pos == "+"
                    self._setPosition(pos, " ")
                    surr_pos = findSurroundings(self.board, pos)
                    for xy in surr_pos:
                        #unnecessary, just to avoid repeated elements
                        #inside the to_check list
                        if xy not in to_check and xy not in checking:
                            to_check.append(xy)

            checking = to_check[:]
            del to_check[:]

    def hadVictory(self):
        for i in self.board:
            if "+" in i:
                return False

        return True

print("Welcome to Minesweeper!\n\n"
      "Symbology:\n"
      "\t[+] = non-neutralized square\n"
      "\t[ ] = neutralized square\n"
      "\t[1],...,[8] = square with N bombs in its surroundings\n"
      "\t[B] = square with bomb")

def play():
    while True:
        size = input("\nSize of the board (between 4 and 20): ")
        if size.isdigit() and 4 <= int(size) <= 20:
            size = int(size)
            break
        print("\nInvalid size!")

    while True:
        mini, maxi = round(size**2 * 1/6), round(size**2 * 4/5)
        n_bombs = input("Number of bombs"
                        " (between {} e {}): ".format(mini, maxi))
        if n_bombs.isdigit() and mini <= int(n_bombs) <= maxi:
            n_bombs = int(n_bombs)
            break
        print("\nInvalid number of bombs!\n")

    board = Board(size, n_bombs)

    #first turn
    board.printBoard()

    while True:
        firsti = input("Square (i) to neutralize: ")
        firstj = input("Square (j) to neutralize: ")
        if firsti.isdigit() and firstj.isdigit() \
           and 0 <= int(firsti) < board.size \
           and 0 <= int(firstj) < board.size:
            firsti, firstj = int(firsti), int(firstj)
            break
        print("\nInvalid position!\n")

    pos = [firsti, firstj]

    board.setBombs(pos)
    board.expandPosition(pos)

    if board.hadVictory():
        board.printBoard(finish=True)
        print("Congratulations, you win! :D\n")
        return

    board.printBoard()

    #turns 2 - n
    while True:

        while True:
            posi = input("Square (i) to neutralize: ")
            posj = input("Square (j) to neutralize: ")
            if posi.isdigit() and posj.isdigit() \
               and 0 <= int(posi) < board.size \
               and 0 <= int(posj) < board.size:
                posi, posj = int(posi), int(posj)
                break
            print("\nInvalid position!\n")

        pos = [posi, posj]

        if board.isBomb(pos):
            board.printBoard(finish=True)
            print("You hit a bomb! :(\n")
            break

        elif board.isNeutral(pos) or board.isNumber(pos):
            print("\nThis square has already been neutralized.")

        else:
            board.expandPosition(pos)
            if board.hadVictory():
                board.printBoard(finish=True)
                print("Congratulations, you win! :)\n")
                break

        board.printBoard()


play()
while True:
    again = input("Type anything to play again"
                    " or type Enter to exit: ")
    if again == "":
        break
    play()

print("\nThank you for playing Minesweeper!\n\t\t\tby Paulo Comasetto")
