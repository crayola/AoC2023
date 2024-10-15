from functools import cache

INPUT = "input"


def parse_record(rec):
    """
    Takes a string `rec` as input, splits it into a list of substrings based on
    spaces, converts the second substring into a tuple of integers based on commas,
    and returns the modified list.

    Args:
        rec (str): Expected to contain a record with a space-separated format,
            where the second element is a comma-separated list of integers.

    Returns:
        List[str|tuple[int]]: A list containing a string and a tuple of integers.

    """
    rec = rec.split(" ")
    rec[1] = tuple([int(x) for x in rec[1].split(",")])
    return rec


def unfold(rec):
    """
    Modifies a record by multiplying its second element by 5 and repeating its
    first element five times, then returns the modified record.

    Args:
        rec (List[str | int]): Represented as a list with at least two elements,
            where the first element is a string and the second element is an integer.

    Returns:
        List[str]: A list containing two elements: the first is a string repeated
        five times, and the second is the original second element multiplied by 5.

    """
    rec[1] = rec[1] * 5
    rec[0] = "?".join([rec[0]] * 5)
    return rec


@cache
def count_possible_solutions(rec, encoding):
    """
    Determines the number of possible solutions for a given regular expression
    `rec` and character encoding `encoding`. It uses recursion and memoization to
    count the possibilities based on the current character in the regular expression.

    Args:
        rec (str): A string representing a record or a sequence of characters that
            is being processed.
        encoding (List[int]): Used to track the length of the remaining encoding.

    Returns:
        int: The number of possible solutions for a given regular expression `rec`
        and encoding `encoding`.

    """
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
