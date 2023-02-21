"""Contains player class."""
import random

from board import Board


class Player:
    """Superclass for players."""

    def __init__(self, letter, opponent):
        """Initialize player with letter."""
        self.letter = letter
        self.opponent = opponent

    def make_move(self, board):
        """Get coordinates for new move."""


class HumanPlayer(Player):
    """User controlled player."""

    def make_move(self, board: Board):
        """Player selects square on the board to fill."""
        square = None
        while not square:
            square = self.select_square(board)
        return square

    def select_square(self, board: Board):
        row_input = input("Choose a row. Rows are indexed at one from top.\n")
        if row_input not in board.valid_row_inputs:
            print("Please enter a valid row number.")
            return None
        col_input = input("Choose a col. Cols are indexed at one from left.\n")
        if col_input not in board.valid_col_inputs:
            print("Please enter a valid col number.")
            return None
        row, col = int(row_input) - 1, int(col_input) - 1
        if board.coords[(row, col)] != " ":
            print("That square is already filled!")
            return None
        return (row, col)


class AiPlayer:
    """Create a cpu player."""

    def __init__(self, letter: str, opponent: str, difficulty: str):
        """Initialize player.

        Args:
            letter (str): Letter that will rep player on board
            opponent (str): opponent's letter
            difficulty (str): how difficult ai will be to beat.
            Difficulties are: easy, normal, chaotic, and master
        """
        self.letter = letter
        self.opponent = opponent
        self.difficulty = difficulty

    def seek_winning_square(self, board: Board):
        """Check if there is a square that would allow self or opponent to win."""
        self_win_square = board.winning_square(self.letter)
        if self_win_square:
            return self_win_square
        opponent_win_square = board.winning_square(self.opponent)
        if opponent_win_square:
            return opponent_win_square
        return None

    def medium_move(self, board: Board) -> tuple:
        """Fill own sreaks and block player streaks, otherwise pick random."""
        winner_square = self.seek_winning_square(board)
        if winner_square:
            return winner_square
        return random.choice(board.get_all_matching(" "))

    def monte_move(self, board: Board):
        """Monte carlo algorithm playing each empty cell 100 times."""
        if self.difficulty == "master":
            # Skip over all the monte carlo if there's a clear winning square.
            winner_square = self.seek_winning_square(board)
            if winner_square:
                return winner_square
        empty_squares = board.get_all_matching(" ")
        # How viable each cell will be.
        cell_scores = {cell: 0 for cell in empty_squares}
        for cell in empty_squares:
            board.fill(cell, self.letter)
            empty_copy = empty_squares[:]
            empty_copy.remove(cell)
            for _ in range(100):
                cell_scores[cell] += self.monte_carlo(board, 0, empty_copy)
            board.fill(cell, " ")
        max_cell = max(cell_scores, key=cell_scores.get)
        min_cell = min(cell_scores, key=cell_scores.get)
        if self.difficulty == "master":
            return max_cell
        if self.difficulty == "easy":
            return min_cell
        return random.choice([max_cell, min_cell])

    def monte_carlo(self, brd: Board, depth: int, empty_squares: list) -> int:
        """Implement the Monte Carlo algorithm."""
        winner = brd.get_winner()
        if winner == self.letter:
            return 1
        if winner == self.opponent:
            return -1
        if brd.is_full():
            return 0
        players = [self.opponent, self.letter]
        to_fill = players[depth % 2]
        fill_square = random.choice(empty_squares)
        new_list = empty_squares[:]
        new_list.remove(fill_square)
        brd.fill(fill_square, to_fill)
        score = self.monte_carlo(brd, depth + 1, new_list)
        brd.fill(fill_square, " ")
        return score

    def make_move(self, brd: Board):
        """Make move on board according to difficulty."""
        difficulty_list = [self.monte_move, self.medium_move]
        if self.difficulty in ["easy", "master"]:
            return difficulty_list[0](brd)
        if self.difficulty == "medium":
            return difficulty_list[1](brd)
        return random.choice(difficulty_list)(brd)
