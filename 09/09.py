def get_prediction(line):
    """
    Calculates a prediction based on a given input line by iteratively computing
    differences between adjacent elements and summing the last element of each
    difference list.

    Args:
        line (List[int]): Represented as a list of integers.

    Returns:
        int: Predicted based on the input list `line`.

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
    Calculates the postdiction of a given sequence of numbers, represented as a
    list `line`. It iteratively computes the differences between adjacent elements
    in the sequence and the differences of those differences, until the differences
    become constant, and then calculates the postdiction by summing the initial
    difference and the alternating sum of the differences of the differences.

    Args:
        line (List[int]): Used as the initial value for the `diff` list, which is
            a list of lists of integers.

    Returns:
        int: The difference between the first element of the last list in the diff
        list and the cumulative sum of differences up to the previous list.

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
