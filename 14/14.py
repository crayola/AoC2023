from tqdm import tqdm
from functools import cache

INPUT = "input"


class Line:
    def __init__(self, line):
        self.line = "".join(line)

    def tilt_once(self):
        self.line = self.line.replace(".O", "O.")

    def tilt(self):
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
    def __init__(self, lines):
        self.lines = [Line(line.strip()) for line in lines.strip().split('\n')]
        self.cols = list(map(Line, zip(*[line.line for line in self.lines])))
        self.n_rows = len(self.lines)
        self.n_cols = len(self.cols)

    @property
    def score(self):
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
        for line in self.lines:
            line.line = line.line[::-1]
            line.tilt()
            line.line = line.line[::-1]
        self.cols = list(map(Line, zip(*[line.line for line in self.lines])))

    def cycle(self):
        self.tilt_north()
        self.tilt_west()
        self.tilt_south()
        self.tilt_east()

    def __repr__(self):
        return "\n".join([line.line for line in self.lines])

@cache
def make_100_cycles(platform_str):
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


