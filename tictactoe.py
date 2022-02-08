"""Tic Tac Toe game in python."""
from board import Board
from player import AiPlayer


def make_board() -> Board:
    """Create board from user input."""
    x_dim, y_dim = "0", "0"
    while not x_dim.isnumeric() or int(x_dim) < 3:
        x_dim = input("Enter board width (must be three or greater)\n")
    while not y_dim.isnumeric() or int(y_dim) < 3:
        y_dim = input("Enter board height (must be three or greater)\n")
    grid = [[' '] * int(x_dim) for i in range(int(y_dim))]
    return Board(grid)


def player_move(brd: Board) -> tuple:
    """Player selects square on the board to fill."""
    valid_rows = [str(i + 1) for i in range(brd.height)]
    valid_cols = [str(i + 1) for i in range(brd.width)]
    while True:
        row_in = input("Choose a row. Rows are indexed at one from top.\n")
        if row_in not in valid_rows:
            print("Please enter a valid row number.")
            continue
        col_in = input("Choose a col. Cols are indexed at one from left.\n")
        if col_in not in valid_cols:
            print("Please enter a valid col number.")
            continue
        row, col = int(row_in) - 1, int(col_in) - 1
        if brd.grid[row][col] == ' ':
            return (row, col)
        print("That square is already filled!")


def difficulty_select() -> str:
    """Select difficulty for the ai."""
    difficulties = {
        "1": "easy", "2": "medium",
        "3": "master", "4": "chaotic"
        }
    while True:
        print("How difficult would you like the ai?\n\
1) Easy\n\
2) Medium\n\
3) Master\n\
4) Chaotic")
        difficulty = input("Difficulty: ")
        if difficulty in difficulties:
            return difficulties[difficulty]
        print("Please enter a number from 1 to 4.")


def main():
    """Play the game."""
    print("Welcome!")
    board = make_board()
    print(board)
    difficulty = difficulty_select()
    ai_1 = AiPlayer('O', 'X', difficulty)
    while True:
        print(board)
        p1_move = player_move(board)
        board.fill_square(p1_move, 'X')
        print(board)
        if board.has_three('X'):
            print("You win!")
            return
        if board.is_full():
            print("Tie!")
            return
        ai_move = ai_1.make_move(board)
        board.fill_square(ai_move, ai_1.letter)
        print(f"\
Cpu player filled in row {ai_move[0]} col {ai_move[1]}.\
        ")
        if board.has_three('O'):
            print(board)
            print("You lose!")
            return
        if board.is_full():
            print(board)
            print("Tie!")
            return


main()
