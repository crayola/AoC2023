from functools import cache

INPUT = "input"


def parse_record(rec):
    """
    Splits a string into a list of space-separated values, converts the second
    value into a tuple of integers separated by commas, and returns the modified
    list.

    Args:
        rec (str): Expected to contain a space-separated string that represents a
            record.

    Returns:
        List[str|int]: A list of strings and/or integers.

    """
    rec = rec.split(" ")
    rec[1] = tuple([int(x) for x in rec[1].split(",")])
    return rec


def unfold(rec):
    """
    Takes a list `rec` as input, multiplies the second element of the list by 5,
    and repeats the first element of the list 5 times, joining the repeated elements
    into a string with '?' as the separator.

    Args:
        rec (List[str]): Indexed from 0. It contains two elements: the first element
            at index 0 is a string, and the second element at index 1 is a number.

    Returns:
        List[Dict[str,Union[str,int]]]: Modified dictionary with '0' key containing
        a string repeated five times and '1' key containing the original integer
        value multiplied by 5.

    """
    rec[1] = rec[1] * 5
    rec[0] = "?".join([rec[0]] * 5)
    return rec


@cache
def count_possible_solutions(rec, encoding):
    """
    Calculates the number of possible solutions to a given regular expression
    matching problem, considering a string of characters with possible matches
    represented by "." (any character), "#" (exactly n characters), and "?" (either
    "." or "#").

    Args:
        rec (str): A recursive representation of a string. It contains information
            about the current position in the string being processed.
        encoding (List[int]): Used to keep track of the length of the strings that
            were previously seen in the current branch of the recursion.

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
