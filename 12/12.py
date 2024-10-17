from functools import cache

INPUT = "input"


def parse_record(rec):
    """
    Splits a given record into a list of values, converts the second value into a
    tuple of integers and returns the modified list.

    Args:
        rec (str): Expected to be a string containing a space-separated record.

    Returns:
        List[str|int]: A list containing two elements: a string and a tuple of integers.

    """
    rec = rec.split(" ")
    rec[1] = tuple([int(x) for x in rec[1].split(",")])
    return rec


def unfold(rec):
    """
    Modifies a given record by multiplying its second element by 5 and duplicating
    its first element five times.

    Args:
        rec (List[str | int]): Expected to contain at least two elements, where
            the first element is a string and the second element is an integer.

    Returns:
        List[str]: A list containing two strings. The first string is the input
        string repeated five times, with each repetition separated by a question
        mark. The second string is the input number multiplied by five.

    """
    rec[1] = rec[1] * 5
    rec[0] = "?".join([rec[0]] * 5)
    return rec


@cache
def count_possible_solutions(rec, encoding):
    """
    Calculates the number of possible solutions for a given regular expression and
    input string, considering '.' matches any character, '#' matches a specific
    length, and '?' matches either '.' or '#'.

    Args:
        rec (str): Representing a string representing a regular expression pattern,
            typically used to encode a possible solution in a recursive descent parser.
        encoding (List[int]): Used to represent the lengths of the characters in
            the sequence to be decoded from the input string.

    Returns:
        int: The number of possible solutions for the given recursive and encoding
        strings.

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
