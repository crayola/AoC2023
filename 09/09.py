def get_prediction(line):
    """
    Generates a prediction based on a given input line of numbers, by iteratively
    calculating the differences between adjacent elements and summing the last
    difference at each depth.

    Args:
        line (List[int]): Represented as a sequence of integers, likely representing
            a line segment in a geometric or numerical context, where each integer
            corresponds to a point's x-coordinate.

    Returns:
        int: The sum of the last element of each difference array calculated at
        each depth.

    """
    diff = [line]
    depth = 0
    while len(set(diff[depth])) != 1:
        diff.append([y - x for x, y in zip(diff[depth][:-1], diff[depth][1:])])
        depth += 1
    pred = 0
    for d in range(depth, -1, -1):
        pred += diff[d][-1]
    return pred


def get_postdiction(line):
    """
    Calculates the postdiction of a given line. It iteratively calculates differences
    between adjacent points in the line, then calculates the first difference of
    the last differences, which represents the postdiction.

    Args:
        line (List[int]): Expected to be a list of consecutive integers representing
            a sequence of numbers.

    Returns:
        int: The predicted value of the sequence in the input line, calculated
        based on the differences between consecutive elements in the sequence.

    """
    diff = [line]
    depth = 0
    while len(set(diff[depth])) != 1:
        diff.append([y - x for x, y in zip(diff[depth][:-1], diff[depth][1:])])
        depth += 1
    pred = 0
    for d in range(depth, -1, -1):
        pred = diff[d][0] - pred
    return pred


INPUT = "input"

if __name__ == "__main__":
    lines = [[int(y) for y in x.strip().split()] for x in open(INPUT).readlines()]

    part1 = 0
    for line in lines:
        part1 += get_prediction(line)
    print(f"part 1: {part1}")

    part2 = 0
    for line in lines:
        part2 += get_postdiction(line)
    print(f"part 2: {part2}")
