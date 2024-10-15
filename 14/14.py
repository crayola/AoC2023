from tqdm import tqdm
from functools import cache

INPUT = "input"


class Line:
    """
    Describes a line of text with a specific formatting convention, where dots and
    'O's are used to represent a line. It provides methods to tilt the line once
    or multiple times, count the number of 'O's, and returns a string representation
    of the line.

    Attributes:
        line (str): Initialized in the `__init__` method by joining the `line`
            parameter into a single string using the `"".join()` method. It stores
            the input string in a normalized format.

    """
    def __init__(self, line):
        self.line = "".join(line)

    def tilt_once(self):
        self.line = self.line.replace(".O", "O.")

    def tilt(self):
        """
        Continuously calls `tilt_once` until the line's orientation stops changing.

        """
        pretilt = self.line
        self.tilt_once()
        while pretilt != self.line:
            pretilt = self.line
            self.tilt_once()

    @property
    def o_count(self):
        """
        Counts the occurrences of the character 'O' in the line.

        Returns:
            int: The number of occurrences of the character 'O' in the string `self.line`.

        """
        return self.line.count('O')

    def __repr__(self):
        return f"Line: {self.line}"


class Platform:
    """
    Represents a two-dimensional grid of lines, where each line is an instance of
    the `Line` class. It provides methods to manipulate the grid through rotations
    and tilts, calculating scores and generating string representations of the grid.

    Attributes:
        lines (List[Line]): Initialized in the `__init__` method. It stores a list
            of `Line` objects, each representing a row of the platform, created
            from input strings after stripping newline characters and splitting
            into individual lines.
        cols (List[Line]): Initialized in the `__init__` method by transposing the
            `lines` attribute using the `zip` function and mapping each row to a
            `Line` object.
        n_rows (int): Initialized in the `__init__` method as the length of the
            `lines` list, which represents the number of rows in the platform.
        n_cols (int): Initialized in the `__init__` method to the length of
            `self.cols`, which is calculated by transposing the `lines` attribute,
            effectively counting the number of columns in the platform.

    """
    def __init__(self, lines):
        """
        Initializes the class with a list of lines, strips newline characters,
        creates Line objects for each line, and creates Line objects for each
        column, storing the number of rows and columns in instance variables.

        Args:
            lines (str | List[str]): Passed to the `__init__` method of the class
                instance.

        """
        self.lines = [Line(line.strip()) for line in lines.strip().split('\n')]
        self.cols = list(map(Line, zip(*[line.line for line in self.lines])))
        self.n_rows = len(self.lines)
        self.n_cols = len(self.cols)

    @property
    def score(self):
        """
        Calculates the overall score of the platform based on the number of occupied
        cells in each line, with a higher score for lines closer to the bottom.

        Returns:
            int: Calculated based on the number of lines in the object, the row
            count of the platform, and the line count of each line in the object.

        """
        score = 0
        for i, line in enumerate(self.lines):
            score += (platform.n_rows - i) * line.o_count
        return score
    
    @property
    def big_string(self):
        """
        Constructs a large string by joining each line of text from the lines
        attribute with a newline character.

        Returns:
            str: A string consisting of all lines in the object, joined by newline
            characters.

        """
        return "\n".join([line.line for line in self.lines]) 

    def tilt_north(self):
        """
        Rotate each column of the platform to their respective tilt angles, then
        recreate the lines of the platform by taking the horizontal cross-sections
        of the tilted columns.

        """
        for col in self.cols:
            col.tilt()
        self.lines = list(map(Line, zip(*[cols.line for cols in self.cols])))

    def tilt_south(self):
        """
        Reverses the orientation of each column's line, applies a tilt transformation,
        and then reverses the line back to its original orientation.

        """
        for col in self.cols:
            col.line = col.line[::-1]
            col.tilt()
            col.line = col.line[::-1]
        self.lines = list(map(Line, zip(*[cols.line for cols in self.cols])))

    def tilt_west(self):
        """
        Tilts each line in the platform to the west and transposes the lines to
        create columns, resulting in a new set of columns that are perpendicular
        to the original lines.

        """
        for line in self.lines:
            line.tilt()
        self.cols = list(map(Line, zip(*[line.line for line in self.lines])))

    def tilt_east(self):
        """
        Reverses the order of characters in each line of a platform, applies a
        tilt transformation to each character, and then reverses the order of
        characters again. It also restructures the platform into columns.

        """
        for line in self.lines:
            line.line = line.line[::-1]
            line.tilt()
            line.line = line.line[::-1]
        self.cols = list(map(Line, zip(*[line.line for line in self.lines])))

    def cycle(self):
        """
        Rotates the platform by tilting it in a clockwise direction, sequentially
        in the north, west, south, and east directions.

        """
        self.tilt_north()
        self.tilt_west()
        self.tilt_south()
        self.tilt_east()

    def __repr__(self):
        return "\n".join([line.line for line in self.lines])

@cache
def make_100_cycles(platform_str):
    """
    Executes a platform's cycle 100 times, caches the results, and returns two
    values: a long string generated by the platform and its final score after the
    cycles.

    Args:
        platform_str (str): Passed to the `Platform` class's constructor to
            initialize a `Platform` object.

    Returns:
        tuple[str,int]: A tuple containing the `big_string` and `score` attributes
        of the `Platform` object after 100 cycles.

    """
    platform = Platform(platform_str)
    for i in range(100):
        platform.cycle()
    return platform.big_string, platform.score


if __name__ == "__main__":
    lines = open(INPUT).read()
    platform = Platform(lines)
    platform.tilt_north()
    print(f"part1: {platform.score}")

    platform_str = platform.big_string
    for i in tqdm(range(10000000)):
        platform_newstr, score = make_100_cycles(platform_str)
        platform_str = platform_newstr

    print(f"part2: {score}")


