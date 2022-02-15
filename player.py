"""Contains player class."""
import random

from numpy import ma
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
            if brd.coords[(row, col)] == ' ':
                return (row, col)
            print("That square is already filled!")


class AiPlayer:
    """Create a cpu player."""

    def __init__(self, letter: str, opponent: str, difficulty: str):
        """Initialize player.
        Args:
            letter (str): Letter that will rep player on board
            difficulty (str): how difficult ai will be to beat.
            Difficulties are: easy, normal, chaotic, and master
        """
        self.letter = letter
        self.opponent = opponent
        self.difficulty = difficulty

    def medium_move(self, brd: Board) -> tuple:
        """Choose first blank square (subject to change)."""
        try_square = brd.winning_square(self.letter)
        if try_square:
            return try_square
        try_square = brd.winning_square(self.opponent)
        if try_square:
            return try_square
        return random.choice(brd.get_all_matching(' '))

    def monte_moron(self, brd: Board):
        """Monte carlo algorithm choosing min score."""
        empty_list = brd.get_all_matching(' ')
        cell_scores = {cell: 0 for cell in empty_list}
        for cell in empty_list:
            brd.fill(cell, self.letter)
            new_list = empty_list[:]
            new_list.remove(cell)
            for i in range(100):
                cell_scores[cell] += self.monte_carlo(brd, 0, new_list)
            brd.fill(cell, ' ')
        min_cell = min(cell_scores, key=cell_scores.get)
        return min_cell

    def monte_move(self, brd: Board):
        """Monte carlo algorithm playing each empty cell 100 times."""
        empty_list = brd.get_all_matching(' ')
        cell_scores = {cell: 0 for cell in empty_list}
        for cell in empty_list:
            brd.fill(cell, self.letter)
            new_list = empty_list[:]
            new_list.remove(cell)
            for i in range(100):
                cell_scores[cell] += self.monte_carlo(brd, 0, new_list)
            brd.fill(cell, ' ')
        max_cell = max(cell_scores, key=cell_scores.get)
        return max_cell

    def monte_carlo(self, brd: Board, depth: int, empty_list: list) -> int:
        """Implementation of the Monte Carlo algorithm."""
        winner = brd.get_winner()
        if winner == self.letter:
            return 1
        if winner == self.opponent:
            return -1
        if brd.is_full():
            return 0
        players = [self.opponent, self.letter]
        to_fill = players[depth % 2]
        fill_square = random.choice(empty_list)
        new_list = empty_list[:]
        new_list.remove(fill_square)
        brd.fill(fill_square, to_fill)
        score = self.monte_carlo(brd, depth+1, new_list)
        brd.fill(fill_square, ' ')
        return score

    def make_move(self, brd: Board):
        """Make move on board according to difficulty."""
        difficulty_list = [self.monte_moron, self.medium_move, self.monte_move]
        if self.difficulty == "easy":
            return difficulty_list[0](brd)
        if self.difficulty == "medium":
            return difficulty_list[1](brd)
        if self.difficulty == "master":
            return difficulty_list[2](brd)
        return random.choice(difficulty_list)(brd)