base = 3
side = base * base


def expandLine(line):
    return line[0] + line[5:9].join([line[1:5] * (base - 1)] * base) + line[9:13]


def create():
    # pattern for a baseline valid solution
    def pattern(r, c):
        return (base * (r % base) + r // base + c) % side

    # randomize rows, columns and numbers (of valid base pattern)
    from random import sample

    def shuffle(s):
        return sample(s, len(s))

    rBase = range(base)
    rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, base * base + 1))

    # produce board using randomized baseline pattern
    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    squares = side * side
    empties = squares * 3 // 4
    for p in sample(range(squares), empties):
        board[p // side][p % side] = 0

    line0 = expandLine("╔═══╤═══╦═══╗")
    line1 = expandLine("║ . │ . ║ . ║")
    line2 = expandLine("╟───┼───╫───╢")
    line3 = expandLine("╠═══╪═══╬═══╣")
    line4 = expandLine("╚═══╧═══╩═══╝")

    symbol = " 1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    nums = [[""] + [symbol[n] for n in row] for row in board]
    print(line0)
    for r in range(1, side + 1):
        print("".join(n + s for n, s in zip(nums[r - 1], line1.split("."))))
        print([line2, line3, line4][(r % side == 0) + (r % base == 0)])
    return board


def is_valid(board, r, c, k):
    not_in_row = k not in board[r]
    not_in_column = k not in [board[i][c] for i in range(9)]
    not_in_box = k not in [board[i][j] for i in range(r // 3 * 3, r // 3 * 3 + 3) for j in
                            range(c // 3 * 3, c // 3 * 3 + 3)]
    return not_in_row and not_in_column and not_in_box


def solve(board, r=0, c=0):
    if r == 9:
        return True
    elif c == 9:
        return solve(board, r + 1, 0)
    elif board[r][c] != 0:
        return solve(board, r, c + 1)
    else:
        for k in range(1, 10):
            if is_valid(board, r, c, k):
                board[r][c] = k
                if solve(board, r, c + 1):
                    return True
                board[r][c] = 0
        return False


def main():
    customBoard = str(input("would you like to enter a custom board? y/n "))
    if customBoard == "y":
        board = []
        print("please fill in the unfinished board row-wise, using 0 to represent an empty square:")

        # for user input
        for i in range(9):  # for loop for row entries
            a = []
            for j in range(9):  # for loop for column entries
                a.append(int(input()))
            board.append(a)

        # for printing the board
        for i in range(9):
            for j in range(9):
                print(board[i][j], end=" ")
            print()
    else:
        board = create()
    action = str(input("would you like to solve this board or create a new board? solve/create "))
    if action == "solve":
        solve(board)
        line0 = expandLine("╔═══╤═══╦═══╗")
        line1 = expandLine("║ . │ . ║ . ║")
        line2 = expandLine("╟───┼───╫───╢")
        line3 = expandLine("╠═══╪═══╬═══╣")
        line4 = expandLine("╚═══╧═══╩═══╝")

        symbol = " 1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        nums = [[""] + [symbol[n] for n in row] for row in board]
        print(line0)
        for r in range(1, side + 1):
            print("".join(n + s for n, s in zip(nums[r - 1], line1.split("."))))
            print([line2, line3, line4][(r % side == 0) + (r % base == 0)])
        again = str(input("would you like to create another board? y/n "))
        if again == "y":
            main()
    if action == "create":
        main()


main()

