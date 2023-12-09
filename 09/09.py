def get_prediction(line):
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
