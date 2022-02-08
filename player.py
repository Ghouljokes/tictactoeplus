"""Contains player class."""
import math
from board import Board


class Player():
    """Superclass for players."""

    def __init__(self, letter, opponent):
        """Initialize player with letter."""
        self.letter = letter
        self.opponent = opponent

    def make_move(self, brd):
        """Get coordinates for new move."""


class HumanPlayer(Player):
    """User controlled player."""

    def make_move(self, brd: Board):
        """Player selects square on the board to fill."""
        valid_rows = [str(i + 1) for i in range(brd.height)]
        valid_cols = [str(i + 1) for i in range(brd.width)]
        while True:
            row_in = input(
                "Choose a row. Rows are indexed at one from top.\n"
                )
            if row_in not in valid_rows:
                print("Please enter a valid row number.")
                continue
            col_in = input(
                "Choose a col. Cols are indexed at one from left.\n"
                )
            if col_in not in valid_cols:
                print("Please enter a valid col number.")
                continue
            row, col = int(row_in) - 1, int(col_in) - 1
            if brd.grid[row][col] == ' ':
                return (row, col)
            print("That square is already filled!")


class AiPlayer:
    """Create a cpu player."""

    def __init__(self, letter: str, opponent: str, difficulty: str):
        """Initialize player.

        Args:
            letter (str): Letter that will rep player on board
            difficulty (str): how difficult ai will be to beat.
            Difficulties are: baby, normal, chaotic, and master
        """
        self.letter = letter
        self.opponent = opponent
        self.difficulty = difficulty

    def easy_move(self, brd: Board):
        """Choose square that gives least chance of winning."""

    def medium_move(self, brd: Board):
        """Choose first blank square (subject to change)."""
        try_square = brd.winning_square(self.letter)
        if try_square:
            return try_square
        try_square = brd.winning_square('X')
        if try_square:
            return try_square
        for i, row in enumerate(brd.grid):
            for j, square in enumerate(row):
                if square == " ":
                    return (i, j)
        return 0

    def master_move(self, brd: Board):
        """Ai finds best possible move."""
        best_score = -(math.inf)
        best_position = None
        all_empty_cells = brd.get_all_empty()
        win_square = brd.winning_square(self.letter)
        if win_square:
            return win_square
        op_square = brd.winning_square(self.opponent)
        if op_square:
            return op_square
        for cell in all_empty_cells:
            brd.fill_square(cell, self.letter)
            new_empty = all_empty_cells[:]
            new_empty.remove(cell)
            score = self.minimax(brd, 0, new_empty)
            brd.fill_square(cell, ' ')
            if score > best_score:
                best_score = score
                best_position = cell
        return best_position

    def minimax(self, brd: Board, depth: int, free_cells: list) -> int:
        """Minimax function."""
        is_max = (depth % 2 == 1)
        if brd.is_full() or depth >= 5:
            return 0
        to_fill = self.letter if is_max else self.opponent
        not_to_fill = self.opponent if is_max else self.letter
        m_mult = -1 if is_max else 1
        best_score = m_mult * math.inf
        win_square = brd.winning_square(to_fill)
        if win_square:
            return -m_mult
        op_square = brd.winning_square(not_to_fill)
        to_check = [op_square] if op_square else free_cells
        for cell in to_check:
            brd.fill_square(cell, to_fill)
            new_list = free_cells[:]
            new_list.remove(cell)
            score = self.minimax(brd, depth+1, new_list)
            brd.fill_square(cell, ' ')
            best_score = m_mult * min((m_mult * best_score, m_mult * score))
        return best_score

    def make_move(self, brd: Board):
        """Make move on board according to difficulty."""
        if self.difficulty == "baby":
            pass
        if self.difficulty == "normal":
            return self.medium_move(brd)
        if self.difficulty == "master":
            return self.master_move(brd)
        return "You've entered an invalid difficulty, dipshit."  # delete later
