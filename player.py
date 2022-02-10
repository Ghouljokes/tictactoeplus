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

    def easy_move(self, brd: Board) -> tuple:
        """Choose square that gives least chance of winning."""
        worst_score = 2
        worst_position = (None, None)
        all_empty_cells = brd.get_all_matching(' ')
        for cell in all_empty_cells:
            brd.fill_square(cell, self.letter)
            new_empty = all_empty_cells[:]
            new_empty.remove(cell)
            score = -self.minimax(brd, 0, new_empty)
            brd.fill_square(cell, ' ')
            if score < worst_score:
                worst_score = score
                worst_position = cell
            if worst_score == -1:
                return worst_position
        return worst_position

    def medium_move(self, brd: Board) -> tuple:
        """Choose first blank square (subject to change)."""
        try_square = brd.winning_square(self.letter)
        if try_square:
            return try_square
        try_square = brd.winning_square('X')
        if try_square:
            return try_square
        return random.choice(brd.get_all_matching(' '))

    def master_move(self, brd: Board) -> tuple:
        """Ai finds best possible move."""
        best_score = -2
        best_position = (None, None)
        all_empty_cells = brd.get_all_matching(' ')
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
            score = -self.minimax(brd, 0, new_empty)
            brd.fill_square(cell, ' ')
            if score > best_score:
                best_score = score
                best_position = cell
            if best_score == 1:
                return best_position
        return best_position

    def minimax(self, brd: Board, depth: int, free_cells: list):
        """Retrun score of a board."""
        is_max = bool(depth & 1)
        max_player = self.letter if is_max else self.opponent
        min_player = self.opponent if is_max else self.letter
        if brd.has_won(max_player):
            return 1
        if brd.has_won(min_player):
            return -1
        if brd.is_full() or depth >= 5:
            return 0
        if brd.winning_square(max_player):
            return 1
        op_square = brd.winning_square(min_player) 
        best_score = -2
        to_check = [op_square] if op_square else free_cells
        for cell in to_check:
            brd.fill_square(cell, max_player)
            new_list = free_cells[:]
            new_list.remove(cell)
            score = -self.minimax(brd, depth+1, new_list)
            brd.fill_square(cell, ' ')
            if score == 1:
                return 1
            best_score = max(best_score, score)
        return best_score

    def make_move(self, brd: Board):
        """Make move on board according to difficulty."""
        difficulty_list = [self.easy_move, self.medium_move, self.master_move]
        if self.difficulty == "easy":
            return difficulty_list[0](brd)
        if self.difficulty == "medium":
            return difficulty_list[1](brd)
        if self.difficulty == "master":
            return difficulty_list[2](brd)
        return random.choice(difficulty_list)(brd)
