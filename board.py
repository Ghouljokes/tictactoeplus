"""Contains the class for the Board object."""


class Board:
    """Tic tac toe board."""

    # def __init__(self, grid: list[list]) -> None:
    def __init__(self, width: int, height: int) -> None:
        """Make board from given dimensions."""
        self.width = width
        self.height = height
        self.grid = [[' '] * width for i in range(height)]
        self.coords = {}
        for row in range(height):
            for col in range(width):
                self.coords[(row, col)] = ' '
        self.adj_table = {
            "N": lambda a, b, dist: (a-dist, b),
            "NE": lambda a, b, dist: (a-dist, b+dist),
            "E": lambda a, b, dist: (a, b+dist),
            "SE": lambda a, b, dist: (a+dist, b+dist),
            "S": lambda a, b, dist: (a+dist, b),
            "SW": lambda a, b, dist: (a+dist, b-dist),
            "W": lambda a, b, dist: (a, b-dist),
            "NW": lambda a, b, dist: (a-dist, b-dist)
        }

    def __repr__(self) -> str:
        """Print the board."""
        rows_to_print = []
        for row in self.grid[:-1]:
            rows_to_print.append(" | ".join(row))
            rows_to_print.append("-|-".join(["-"] * self.width))
        rows_to_print.append(" | ".join(self.grid[-1]))
        return "\n" + "\n".join(rows_to_print) + "\n"

    def adj(self, position: tuple, direction: str, dist: int = 1) -> str:
        """Return contents of square in direction & distance to pos."""
        row, col = position
        row2, col2 = self.adj_table[direction](row, col, dist)
        if row2 < 0 or col2 < 0 or row2 >= self.height or col2 >= self.width:
            return "None"
        return self.coords[(row2, col2)]

    def fill_square(self, position: tuple, letter: str) -> None:
        """Fill position given by pos in the form (row, col) with a letter."""
        row, col = position
        self.grid[row][col] = letter
        self.coords[position] = letter

    def get_all_empty(self) -> list:
        """Return list of positions for all empty squares in the board."""
        list_of_empty = []
        for i, row in enumerate(self.grid):
            for j, col in enumerate(row):
                if col == ' ':
                    list_of_empty.append((i, j))
        return list_of_empty

    def is_full(self) -> bool:
        """Check if all squares in the board are filled."""
        for row in self.grid:
            if ' ' in row:
                return False
        return True

    def has_three(self, ltr: str) -> bool:
        """Check to see if there's a row of three of the same letter (ltr)."""
        for i, row in enumerate(self.grid):
            for j, col in enumerate(row):
                if col != ltr:
                    continue
                pos = (i, j)
                for k in ["E", "S", "SE", "SW"]:
                    if self.adj(pos, k) == ltr and self.adj(pos, k, 2) == ltr:
                        return True
        return False

    def winning_square(self, ltr: str):
        """Look for a square to put letter to win the game."""
        for i, row in enumerate(self.grid):
            for j, col in enumerate(row):
                if col != ltr:
                    continue
                pos = (i, j)
                for k in ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]:
                    if self.adj(pos, k) == ltr and self.adj(pos, k, 2) == ' ':
                        return self.adj_table[k](pos[0], pos[1], 2)
                    if self.adj(pos, k) == ' ' and self.adj(pos, k, 2) == ltr:
                        return self.adj_table[k](pos[0], pos[1], 1)
        return None
