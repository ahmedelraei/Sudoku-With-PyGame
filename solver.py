""" board = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
] """

def print_board(board):
    for x in range(len(board)):
        if x % 3 == 0 and x != 0:
            print("- - - - - - - - - - - - - ")
        for y in range(len(board[0])):
            if y % 3 == 0 and y != 0:
                print(" | ", end="")

            if y == 8:
                print(board[x][y])
            else:
                print(str(board[x][y]) + " ", end="")


def locate_empty(board):
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] == 0:
                return (x, y)
    
    return None



def validate(board, num, pos):
    # Check row
    for y in range(len(board[0])):
        if board[pos[0]][y] == num and pos[1] != y:
            return False

    # Check column
    for x in range(len(board)):
        if board[x][pos[1]] == num and pos[0] != x:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for x in range(box_y*3, box_y*3 + 3):
        for y in range(box_x*3, box_x*3 + 3):
            if board[x][y] == num and (x,y) != pos:
                return False
    
    return True

def solve(board):
    find = locate_empty(board)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1,10):
        if validate(board, i, (row,col)):
            board[row][col] = i

            if solve(board):
                return True

            board[row][col] = 0
    
    return False

""" print_board(board)
solve(board)
print("\n ============================ \n")
print_board(board) """