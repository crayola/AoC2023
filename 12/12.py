from functools import cache

INPUT = "input"


def parse_record(rec):
    rec = rec.split(" ")
    rec[1] = tuple([int(x) for x in rec[1].split(",")])
    return rec


def unfold(rec):
    rec[1] = rec[1] * 5
    rec[0] = "?".join([rec[0]] * 5)
    return rec


@cache
def count_possible_solutions(rec, encoding):
    if rec == "":
        return 1 if len(encoding) == 0 else 0
    if len(encoding) == 0:
        return 0 if "#" in rec else 1
    if rec[0] == ".":
        return count_possible_solutions(rec[1:], encoding)
    if rec[0] == "#":
        if len(rec) < encoding[0] or "." in rec[: encoding[0]]:
            return 0
        if len(rec) == encoding[0]:
            return 1 if len(encoding) == 1 else 0
        if rec[encoding[0]] == "#":
            return 0
        return count_possible_solutions(rec[encoding[0] + 1 :], encoding[1:])
    if rec[0] == "?":
        return count_possible_solutions(
            "." + rec[1:], encoding
        ) + count_possible_solutions("#" + rec[1:], encoding)


if __name__ == "__main__":
    records = [parse_record(x) for x in open(INPUT).readlines()]

    # part 1
    part1 = 0
    for rec in records:
        part1 += count_possible_solutions(rec[0], rec[1])
    print(f"part 1: {part1}")

    # part 2
    part2 = 0
    for rec in records:
        unfold(rec)
        part2 += count_possible_solutions(rec[0], rec[1])

    print(f"part 2: {part2}")
