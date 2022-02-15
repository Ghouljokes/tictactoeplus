
"""Contains the class for the Board object."""


class Board:
    """Tic tac toe board."""

    def __init__(self, width: int, height: int) -> None:
        """Make board from given dimensions."""
        self.width = width
        self.height = height
        self.coords: dict = {}
        self.letters = ["X", "O"]
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
        self.func_counts = {
            "get_match": 0, "is_full": 0, "get_streak": 0, 
            "get_winner": 0, "win_square": 0
        }
        self.corner_dirs = {
            (0, 0): "SE",
            (0, width-1): "SW"
        }
        if self.height != self.width:
            self.corner_dirs[(height-1, width-1)] = "NW"
            self.corner_dirs[(height-1, 0)] = "NE"
        self.all_paths = []
        for row in range(height):
            new_row = [(row, col) for col in range(width)]
            self.all_paths.append(new_row)
        for col in range(width):
            new_col = [(row, col) for row in range(height)]
            self.all_paths.append(new_col)
        for pos, direction in self.corner_dirs.items():
            new_ray = self.get_streak(pos, direction)
            self.all_paths.append(new_ray)


    def __repr__(self) -> str:
        """Print the board."""
        rows_to_print = []
        for row in range(self.height):
            to_print = [self.coords[(row, col)] for col in range(self.width)]
            rows_to_print.append(" | ".join(to_print))
        separator = f"\n{'-|-'.join(['-'] * self.width)}\n"
        return f"\n{separator.join(rows_to_print)}\n"

    def fill(self, position: tuple[int, int], letter: str) -> None:
        """Fill position given by pos in the form (row, col) with a letter."""
        self.coords[position] = letter

    def get_all_matching(self, ltr: str) -> list:
        """Return list of positions for all squares with val ltr."""
        self.func_counts["get_match"] += 1
        list_of_empty = [pos for pos, val in self.coords.items() if val == ltr]
        return list_of_empty

    def is_full(self) -> bool:
        """Check if all squares in the board are filled."""
        self.func_counts["is_full"] += 1
        return ' ' not in self.coords.values()

    def get_streak(self, pos: tuple, direction: str) -> list:
        """Return a list of all coords in a line from a position."""
        self.func_counts["get_streak"] += 1
        i = 1
        streak = [pos]
        while True:
            new_square = self.adj_table[direction](pos[0], pos[1], i)
            if new_square not in self.coords:
                return streak
            streak.append(new_square)
            i += 1

    def get_winner(self):
        """Check to see if there is a winner."""
        self.func_counts["get_winner"] += 1
        for path in self.all_paths:
            vals = [self.coords[cell] for cell in path]
            for letter in self.letters:
                if vals.count(letter) == len(vals):
                    return letter
        return None

    def winning_square(self, ltr: str):
        """Return position ltr should place to win."""
        self.func_counts["win_square"] += 1
        if len(self.get_all_matching(ltr)) < min([self.width, self.height]) - 1:
            return None
        for path in self.all_paths:
           vals = [self.coords[cell] for cell in path]
           if vals.count(' ') == 1 and vals.count(ltr) == len(vals) - 1:
               return path[vals.index(' ')]
        return None