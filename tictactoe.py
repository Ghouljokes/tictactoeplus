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


def player_move(brd: Board):
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


def main():
    """Play the game."""
    print("Welcome!")
    board = make_board()
    print(board)

    ai_1 = AiPlayer('O', 'X', "master")
    while not board.is_full():
        if not board.has_three(ai_1.letter):
            p_move = player_move(board)
            board.fill_square((p_move), 'X')
            print(board)
        else:
            print(f'Sorry, {ai_1.letter} won this time!')
            break

        if not board.has_three('X') and not board.is_full():
            move = ai_1.make_move(board)
            if move == 0:
                print('Tie Game!')
            board.fill_square(move, ai_1.letter)
            row = move[0] + 1
            col = move[1] + 1
            print(f"Computer places {ai_1.letter} in row {row}, col {col}")
            print(board)
        else:
            print('X wins! Hell yea.')
            break

    if board.is_full():
        print("Tie!")


main()
