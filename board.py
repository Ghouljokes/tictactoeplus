"""Contains the class for the Board object."""


class Board:
    """Tic tac toe board."""

    def __init__(self, width: int, height: int) -> None:
        """Make board from given dimensions."""
        self.width = width
        self.height = height
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
        for row in range(self.height):
            to_print = [self.coords[(row, col)] for col in range(self.width)]
            rows_to_print.append(" | ".join(to_print))
        separator = f"\n{'-|-'.join(['-'] * self.width)}\n"
        return f"\n{separator.join(rows_to_print)}\n"

    def adj(self, position: tuple, direction: str, dist: int = 1) -> str:
        """Return contents of square in direction & distance to pos."""
        row, col = position
        row2, col2 = self.adj_table[direction](row, col, dist)
        if row2 < 0 or col2 < 0 or row2 >= self.height or col2 >= self.width:
            return "None"
        return self.coords[(row2, col2)]

    def fill_square(self, position: tuple[int, int], letter: str) -> None:
        """Fill position given by pos in the form (row, col) with a letter."""
        self.coords[position] = letter

    def get_all_empty(self) -> list:
        """Return list of positions for all empty squares in the board."""
        list_of_empty = [pos for pos, val in self.coords.items() if val == ' ']
        return list_of_empty

    def is_full(self) -> bool:
        """Check if all squares in the board are filled."""
        return ' ' not in self.coords.values()

    def has_three(self, ltr: str) -> bool:
        """Check to see if there's a row of three of the same letter (ltr)."""
        for pos, val in self.coords.items():
            if val != ltr:
                continue
            for i in ["E", "S", "SE", "SW"]:
                if self.adj(pos, i) == ltr and self.adj(pos, i, 2) == ltr:
                    return True
        return False

    def winning_square(self, ltr: str):
        """Look for a square to put letter to win the game."""
        for pos, val in self.coords.items():
            if val != ltr:
                continue
            for i in ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]:
                if self.adj(pos, i) == ltr and self.adj(pos, i, 2) == ' ':
                    return self.adj_table[i](pos[0], pos[1], 2)
                if self.adj(pos, i) == ' ' and self.adj(pos, i, 2) == ltr:
                    return self.adj_table[i](pos[0], pos[1], 1)
        return None
