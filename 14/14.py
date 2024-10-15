from tqdm import tqdm
from functools import cache

INPUT = "input"


class Line:
    """
    Represents a line of text with a dynamic 'O' character placement. It can be
    tilted by swapping '.O' with 'O.' until no further changes occur. The class
    also tracks the total 'O' count and provides a string representation of the line.

    Attributes:
        line (str): Initialized in the `__init__` method by joining the input
            `line` parameter into a single string, which is then stored in the
            `line` attribute of the class instance.

    """
    def __init__(self, line):
        self.line = "".join(line)

    def tilt_once(self):
        self.line = self.line.replace(".O", "O.")

    def tilt(self):
        """
        Iterates until the line's orientation is stable, indicating no further
        tilting is needed.

        """
        pretilt = self.line
        self.tilt_once()
        while pretilt != self.line:
            pretilt = self.line
            self.tilt_once()

    @property
    def o_count(self):
        return self.line.count('O')

    def __repr__(self):
        return f"Line: {self.line}"


class Platform:
    """
    Represents a 2D grid of lines, where each line is an instance of the `Line`
    class. It provides properties to calculate the score and a string representation
    of the platform, as well as methods to tilt the platform and cycle through
    different orientations.

    Attributes:
        lines (List[Line]): Initialized in the `__init__` method. It contains a
            list of `Line` objects, where each `Line` object represents a row of
            the platform, stripped of leading and trailing whitespace.
        cols (List[Line]): Created by transposing the `lines` attribute, effectively
            treating each column of the original grid as a single line.
        n_rows (int): Calculated as the number of elements in the list `self.lines`,
            which represents the rows of the platform.
        n_cols (int): Calculated as the number of columns in the platform, which
            is the length of the list of column objects (`self.cols`).

    """
    def __init__(self, lines):
        """
        Initialize a platform object. It takes a string of text as input, splits
        it into lines, and then splits each line into columns. It stores the lines
        and columns in the instance variables `self.lines` and `self.cols` respectively.

        Args:
            lines (str | List[str]): Initialized with a string or a list of strings,
                where each string represents a line of text.

        """
        self.lines = [Line(line.strip()) for line in lines.strip().split('\n')]
        self.cols = list(map(Line, zip(*[line.line for line in self.lines])))
        self.n_rows = len(self.lines)
        self.n_cols = len(self.cols)

    @property
    def score(self):
        """
        Calculates the total score of the platform by iterating over its lines,
        where each line's score is determined by its position and the number of
        objects on it.

        Returns:
            int: Calculated based on the number of lines, their positions, and the
            number of objects (`o_count`) in each line.

        """
        score = 0
        for i, line in enumerate(self.lines):
            score += (platform.n_rows - i) * line.o_count
        return score
    
    @property
    def big_string(self):
        return "\n".join([line.line for line in self.lines]) 

    def tilt_north(self):
        for col in self.cols:
            col.tilt()
        self.lines = list(map(Line, zip(*[cols.line for cols in self.cols])))

    def tilt_south(self):
        """
        Reverses the order of each line segment within each column, applies a tilt
        transformation, and then reverses the order again. It then generates new
        line segments for the platform by transposing the lines of the columns.

        """
        for col in self.cols:
            col.line = col.line[::-1]
            col.tilt()
            col.line = col.line[::-1]
        self.lines = list(map(Line, zip(*[cols.line for cols in self.cols])))

    def tilt_west(self):
        for line in self.lines:
            line.tilt()
        self.cols = list(map(Line, zip(*[line.line for line in self.lines])))

    def tilt_east(self):
        """
        Reverses the characters in each line of a platform, tilts each line, and
        then reverses the characters back to their original order, effectively
        tilting the platform eastward.

        """
        for line in self.lines:
            line.line = line.line[::-1]
            line.tilt()
            line.line = line.line[::-1]
        self.cols = list(map(Line, zip(*[line.line for line in self.lines])))

    def cycle(self):
        """
        Rotates the platform through four positions:
        - Tilt north
        - Tilt west
        - Tilt south
        - Tilt east.

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
    Cycles a `Platform` object 100 times based on the provided `platform_str`, and
    returns the resulting `big_string` and `score`.

    Args:
        platform_str (str): Used to initialize a Platform object with the specified
            platform string.

    Returns:
        Tuple[str,int]: A tuple containing two elements: `big_string` of type `str`
        and `score` of type `int`.

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


