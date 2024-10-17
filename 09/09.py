def get_prediction(line):
    """
    Calculates a prediction based on a given input `line` by iteratively applying
    a difference operation and summing the resulting values.

    Args:
        line (List[int]): Assumed to be a list of consecutive integers representing
            a sequence where each integer is the difference between two adjacent
            elements in the sequence.

    Returns:
        int: Predicted based on a sequence of numbers input as a list `line`.

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
    Calculates the postdiction of a given sequence. It iteratively computes
    differences between consecutive elements at each level, until all elements at
    a level are identical. The postdiction is then calculated by summing these
    differences in reverse order.

    Args:
        line (List[int]): Assumed to represent a list of consecutive integer values,
            likely representing a sequence of numbers with some pattern or trend.

    Returns:
        int: A prediction based on the differences in a given sequence, specifically
        the last difference that would result in a single unique value in the sequence.

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
