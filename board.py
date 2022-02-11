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
        if height != width:
            self.corner_dirs[(height-1, width-1)] = "NW"
            self.corner_dirs[(height-1, 0)] = "NE"
        self.all_possible_paths = []
        for row in range(height):
            poss_row = self.get_streak((row, 0), 'E')
            self.all_possible_paths.append(poss_row)
        for col in range(width):
            poss_col = self.get_streak((0, col), "S")
            self.all_possible_paths.append(poss_col)
        for corner, direction in self.corner_dirs.items():
            poss_streak = self.get_streak(corner, direction)
            self.all_possible_paths.append(poss_streak)

    def __repr__(self) -> str:
        """Print the board."""
        rows_to_print = []
        for row in range(self.height):
            to_print = [self.coords[(row, col)] for col in range(self.width)]
            rows_to_print.append(" | ".join(to_print))
        separator = f"\n{'-|-'.join(['-'] * self.width)}\n"
        return f"\n{separator.join(rows_to_print)}\n"

    def fill_square(self, position: tuple[int, int], letter: str) -> None:
        """Fill position given by pos in the form (row, col) with a letter."""
        self.coords[position] = letter

    def get_all_matching(self, ltr: str) -> list:
        """Return list of positions for all squares with val ltr."""
        return [pos for pos, val in self.coords.items() if val == ltr]

    def is_full(self) -> bool:
        """Check if all squares in the board are filled."""
        return ' ' not in self.coords.values()

    def get_streak(self, pos: tuple, direction: str) -> list:
        """Return a list of all coords in a line from a position."""
        if direction in ["N", "S"]:
            return [(row, pos[1]) for row in range(self.height)]
        if direction in ["E", "W"]:
            return [(pos[0], col) for col in range(self.width)]
        i = 1
        streak = [pos]
        while True:
            new_square = self.adj_table[direction](pos[0], pos[1], i)
            if new_square not in self.coords:
                return streak
            streak.append(new_square)
            i += 1

    def has_won(self, ltr: str):
        """Check to see if ltr has won."""
        for path in self.all_possible_paths:
            if all(self.coords[i] == ltr for i in path):
                return True
        return False

    def winning_square(self, ltr: str):
        """Return square that will win the game, if it exists."""
        for path in self.all_possible_paths:
            vals = [self.coords[cell] for cell in path]
            if vals.count(' ') == 1 and vals.count(ltr) == len(vals) - 1:
                return path[vals.index(' ')]
        return None

    def can_win(self, ltr: str):
        """Check if a win is possible."""
        for path in self.all_possible_paths:
            vals = [self.coords[cell] in [' ', ltr] for cell in path]
            if all(vals):
                return True
        return False
