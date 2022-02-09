"""Contains the class for the Board object."""


class Board:
    """Tic tac toe board."""

    def __init__(self, width: int, height: int) -> None:
        """Make board from given dimensions."""
        self.width = width
        self.height = height
        self.coords: dict = {}
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
        self.corner_dirs = {
            (0, 0): "SE",
            (0, width-1): "SW"
        }
        if self.height != self.width:
            self.corner_dirs[(height-1, width-1)] = "NW"
            self.corner_dirs[(height-1, 0)] = "NE"

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

    def get_all_matching(self, ltr: str) -> list:
        """Return list of positions for all squares with val ltr."""
        list_of_empty = [pos for pos, val in self.coords.items() if val == ltr]
        return list_of_empty

    def is_full(self) -> bool:
        """Check if all squares in the board are filled."""
        return ' ' not in self.coords.values()

    def check_streak(self, pos: tuple, ltr: str, direction: str) -> bool:
        """Check if there is a streak across the board at pos in direction."""
        if self.coords[pos] != ltr:
            return False
        new_pos = self.adj_table[direction](pos[0], pos[1], 1)
        if new_pos not in self.coords:
            return True
        return self.check_streak(new_pos, ltr, direction)

    def get_streak(self, pos: tuple, direction: str) -> list:
        """Return a list of all coords in a line from a position."""
        i = 1
        streak = [pos]
        while True:
            new_square = self.adj_table[direction](pos[0], pos[1], i)
            if new_square not in self.coords:
                return streak
            streak.append(new_square)
            i += 1

    def has_won(self, ltr: str) -> bool:
        """Check to see if there's a row of the same ltr accross board."""
        for row in range(self.height):
            chk_row = [(row, col) for col in range(self.width)]
            if all(self.coords[i] == ltr for i in chk_row):
                return True
        for col in range(self.width):
            chk_col = [(row, col) for row in range(self.height)]
            if all(self.coords[i] == ltr for i in chk_col):
                return True
        for corner, direction in self.corner_dirs.items():
            if self.check_streak(corner, ltr, direction):
                return True
        return False

    def winning_square(self, ltr: str):
        """Look for a square that will win the game."""
        letter_coords = self.get_all_matching(ltr)
        if len(letter_coords) < min((self.height, self.width)) - 1:
            return None
        chk_rows = set(coord[0] for coord in letter_coords)
        chk_cols = set(coord[1] for coord in letter_coords)
        if len(chk_rows) < self.height - 1 and len(chk_cols) < self.width - 1:
            return None
        for row in chk_rows:
            chk_row = [(row, col) for col in range(self.width)]
            vals = [self.coords[cell] for cell in chk_row]
            if vals.count(' ') == 1 and vals.count(ltr) == len(vals) - 1:
                return chk_row[vals.index(' ')]
        for col in chk_cols:
            chk_col = [(row, col) for row in range(self.height)]
            vals = [self.coords[cell] for cell in chk_col]
            if vals.count(' ') == 1 and vals.count(ltr) == len(vals) - 1:
                return chk_col[vals.index(' ')]
        for corner, direction in self.corner_dirs.items():
            streak = self.get_streak(corner, direction)
            vals = [self.coords[cell] for cell in streak]
            if vals.count(' ') == 1 and vals.count(ltr) == len(vals) - 1:
                return streak[vals.index(' ')]
        return None
