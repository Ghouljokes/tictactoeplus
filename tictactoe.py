"""Tic Tac Toe game in python."""
from board import Board
from player import AiPlayer, HumanPlayer


def make_board() -> Board:
    """Create board from user input."""
    x_dim, y_dim = "0", "0"
    while not x_dim.isnumeric() or int(x_dim) < 3:
        x_dim = input("Enter board width (must be three or greater)\n")
    while not y_dim.isnumeric() or int(y_dim) < 3:
        y_dim = input("Enter board height (must be three or greater)\n")
    return Board(int(x_dim), int(y_dim))


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
    pl_1 = HumanPlayer('X', 'O')
    ai_1 = AiPlayer('O', 'X', difficulty)
    while True:
        print(board)
        p1_move = pl_1.make_move(board)
        board.fill_square(p1_move, pl_1.letter)
        print(board)
        if board.get_winner() == pl_1.letter:
            print("You win!")
            return
        if board.is_full():
            print("Tie!")
            return
        ai_move = ai_1.make_move(board)
        print(board.func_counts)
        board.fill_square(ai_move, ai_1.letter)
        print(f"\
Cpu player filled in row {ai_move[0]} col {ai_move[1]}.\
        ")
        if board.get_winner() == ai_1.letter:
            print(board)
            print("You lose!")
            return
        if board.is_full():
            print(board)
            print("Tie!")
            return


while True:
    main()
    to_quit = input("Enter \'q\' to quit or any other key to play again.\n")
    if to_quit == 'q':
        break
