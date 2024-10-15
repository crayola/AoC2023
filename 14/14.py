from tqdm import tqdm
from functools import cache

INPUT = "input"


class Line:
    """
    Represents a line of text with operations to manipulate its content. It can
    be tilted by moving dots between Os, and it tracks the count of Os in the line.
    The `__repr__` method provides a string representation of the line.

    Attributes:
        line (str): Initialized in the `__init__` method by joining all elements
            of the `line` parameter into a single string using `"".join(line)`.

    """
    def __init__(self, line):
        """
        Initializes the object by joining the input line into a single string.

        Args:
            line (List[str]): Expected to be a list of strings representing
                individual characters or words in a line of text.

        """
        self.line = "".join(line)

    def tilt_once(self):
        """
        Reverses the position of the 'O' character in the line string, swapping
        it from the end to the start or vice versa, effectively creating a tilt effect.

        """
        self.line = self.line.replace(".O", "O.")

    def tilt(self):
        """
        Rotates the line by continuously calling the `tilt_once` method until it
        reaches a stable position, where the line's orientation has not changed
        since the last call.

        """
        pretilt = self.line
        self.tilt_once()
        while pretilt != self.line:
            pretilt = self.line
            self.tilt_once()

    @property
    def o_count(self):
        """
        Counts the occurrences of the character 'O' in a given line of text.

        Returns:
            int: The count of all occurrences of the character 'O' in the string
            `self.line`.

        """
        return self.line.count('O')

    def __repr__(self):
        """
        Returns a string representation of the Line object, displaying the value
        of its 'line' attribute.

        Returns:
            str: A string representation of the object, specifically in the format
            "Line: <self.line>" where <self.line> is the value of the object's
            line attribute.

        """
        return f"Line: {self.line}"


class Platform:
    """
    Represents a 2D grid of lines, where each line is an instance of the `Line`
    class. It provides methods to manipulate the grid, including tilting, rotating,
    and cycling the lines, as well as calculating a score based on the grid's configuration.

    Attributes:
        lines (List[Line]): Initialized in the `__init__` method. It contains a
            list of `Line` objects, one for each row of the platform, with each
            `Line` object representing a row of characters.
        cols (List[Line]): Initialized in the `__init__` method by transposing the
            `lines` attribute, which is a list of `Line` objects, using the `zip`
            function and the `map` function.
        n_rows (int): Initialized with the length of the `lines` attribute, which
            represents the number of rows in the platform.
        n_cols (int): Derived from the number of columns in the platform, calculated
            as the length of the `cols` list, which is a list of `Line` objects
            transposed from the original lines.

    """
    def __init__(self, lines):
        """
        Initialize a Platform instance. It takes a string of lines as input, parses
        it into a list of Line objects, and creates columns by transposing the
        lines. It also calculates the number of rows and columns.

        Args:
            lines (str | List[str]): Initialized with the contents of a file or a
                string containing newline-separated lines.

        """
        self.lines = [Line(line.strip()) for line in lines.strip().split('\n')]
        self.cols = list(map(Line, zip(*[line.line for line in self.lines])))
        self.n_rows = len(self.lines)
        self.n_cols = len(self.cols)

    @property
    def score(self):
        """
        Calculates a score based on the number of occupied cells in each line of
        the platform, with each line's contribution weighted by its distance from
        the top.

        Returns:
            int: Calculated by multiplying the number of remaining rows by the
            number of occupied cells in each line and summing these products.

        """
        score = 0
        for i, line in enumerate(self.lines):
            score += (platform.n_rows - i) * line.o_count
        return score
    
    @property
    def big_string(self):
        """
        Concatenates the content of all lines in the Platform instance's `lines`
        attribute into a single string, with each line separated by a newline
        character, and returns it.

        Returns:
            str|None: A string containing all the lines of a collection of lines,
            separated by newline characters.

        """
        return "\n".join([line.line for line in self.lines]) 

    def tilt_north(self):
        """
        Tilts each column and then rearranges the lines to be perpendicular to the
        columns, effectively rotating the platform to face north.

        """
        for col in self.cols:
            col.tilt()
        self.lines = list(map(Line, zip(*[cols.line for cols in self.cols])))

    def tilt_south(self):
        """
        Reverses the line of each column, applies the tilt operation, and then
        reverses the line back to its original orientation. It then rearranges the
        lines of the columns into rows.

        """
        for col in self.cols:
            col.line = col.line[::-1]
            col.tilt()
            col.line = col.line[::-1]
        self.lines = list(map(Line, zip(*[cols.line for cols in self.cols])))

    def tilt_west(self):
        """
        Rotates each line in the platform to the left by calling the `tilt` method
        on each line. It then transposes the lines to create new columns and
        reinitializes the `cols` attribute with the new column objects.

        """
        for line in self.lines:
            line.tilt()
        self.cols = list(map(Line, zip(*[line.line for line in self.lines])))

    def tilt_east(self):
        """
        Reverses each line of the platform, applies a tilt operation, and then
        reverses the line back to its original state. It then re-generates the
        columns of the platform by transposing the reversed lines and creating new
        Line objects.

        """
        for line in self.lines:
            line.line = line.line[::-1]
            line.tilt()
            line.line = line.line[::-1]
        self.cols = list(map(Line, zip(*[line.line for line in self.lines])))

    def cycle(self):
        """
        Rotates the platform through four cardinal directions.

        """
        self.tilt_north()
        self.tilt_west()
        self.tilt_south()
        self.tilt_east()

    def __repr__(self):
        """
        Converts the object into a string representation, displaying each line of
        the self.lines collection on a separate line, effectively creating a
        readable, formatted string of the object's contents.

        Returns:
            str: A string representation of the object, specifically a formatted
            representation of all lines in the object's `lines` attribute, separated
            by newline characters.

        """
        return "\n".join([line.line for line in self.lines])

@cache
def make_100_cycles(platform_str):
    """
    Cycles a `Platform` object 100 times based on the input `platform_str`, and
    returns the resulting `big_string` and `score` attributes of the `Platform`
    object after the cycles.

    Args:
        platform_str (str): Used to initialize a `Platform` object, which is then
            used to perform cycles.

    Returns:
        Tuple[str,int]: A tuple containing two elements:
        1/ A string, representing the result of `platform.big_string` after 100 cycles.
        2/ An integer, representing the result of `platform.score` after 100 cycles.

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


