def get_prediction(line):
    """
    Calculates a prediction based on a given input `line`. It generates a series
    of differences in the input values and sums the last value of each difference
    series to produce the prediction.

    Args:
        line (List[int]): Represented as a list of integers, where each integer
            in the list represents a value in a sequence.

    Returns:
        int: A prediction based on the input sequence `line`.

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
    differences between elements in the sequence, stops when differences are
    constant, and then calculates the final postdiction by summing up differences
    in reverse order.

    Args:
        line (List[int]): Represented as a list of integers, presumably representing
            a sequence of values.

    Returns:
        int: The difference between the first element of the last difference list
        and the initial prediction, calculated by subtracting the previous prediction
        from the first element of each difference list, working backwards from the
        last list.

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
