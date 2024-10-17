from pathlib import Path

input_path = Path("./input")


def is_symbol(ch):
    """
    Determines whether a given character is a symbol, excluding digits and periods.
    It returns `True` for all characters except digits and periods, which are
    considered symbols in this context.

    Args:
        ch (str): Represented as a single character.

    Returns:
        bool: True if the input character is a non-digit and not a period, and
        False otherwise.

    """
    if ch.isdigit() or ch == ".":
        return False
    else:
        return True


def get_number(i, j, lines):
    """Get full number containing the digit found at i,j"""
    number = lines[i][j]
    # to the left
    k = 1
    while lines[i][j - k].isdigit():
        number = lines[i][j - k] + number
        k += 1
    # to the right
    k = 1
    while lines[i][j + k].isdigit():
        number = number + lines[i][j + k]
        k += 1
    return int(number)


def get_surrounding_numbers(i, j, lines):
    """
    Recursively retrieves all numbers in the surrounding cells of a given position
    on a grid, considering both horizontal and vertical neighbors, as well as
    diagonals when the immediate top neighbor is not a number.

    Args:
        i (int): Used to represent the row index of a cell in a two-dimensional
            grid or list of lines.
        j (int): Used to represent the column index in a 2D list (`lines`) of a
            number to be checked for surrounding numbers.
        lines (List[List[str]]): Expected to represent a 2D grid or matrix of strings.

    Returns:
        List[int]: A list of surrounding numbers found at the specified position
        `(i, j)` in the given `lines`.

    """
    surrounding_numbers = []
    if lines[i - 1][j].isdigit():
        surrounding_numbers.append(get_number(i - 1, j, lines))
    else:
        if lines[i - 1][j - 1].isdigit():
            surrounding_numbers.append(get_number(i - 1, j - 1, lines))
        if lines[i - 1][j + 1].isdigit():
            surrounding_numbers.append(get_number(i - 1, j + 1, lines))
    if lines[i][j - 1].isdigit():
        surrounding_numbers.append(get_number(i, j - 1, lines))
    if lines[i][j + 1].isdigit():
        surrounding_numbers.append(get_number(i, j + 1, lines))
    if lines[i + 1][j].isdigit():
        surrounding_numbers.append(get_number(i + 1, j, lines))
    else:
        if lines[i + 1][j - 1].isdigit():
            surrounding_numbers.append(get_number(i + 1, j - 1, lines))
        if lines[i + 1][j + 1].isdigit():
            surrounding_numbers.append(get_number(i + 1, j + 1, lines))
    return surrounding_numbers


if __name__ == "__main__":
    raw_lines = open(input_path).readlines()
    n_rows = len(raw_lines) + 2
    n_cols = len(raw_lines[0]) + 2
    lines = ["." * n_cols]
    for line in raw_lines:
        lines.append("." + line.strip() + ".")
    lines.append("." * n_cols)

    part1_sum = 0
    for i, line in enumerate(lines):
        if i == 0 or i == n_rows - 1:
            continue
        running_number = ""
        has_symbol = False
        for j, ch in enumerate(line):
            if j == 0:
                continue
            if not ch.isdigit():
                if running_number:
                    if (
                        is_symbol(lines[i - 1][j])
                        or is_symbol(lines[i][j])
                        or is_symbol(lines[i + 1][j])
                    ):
                        has_symbol = True
                if running_number and has_symbol:
                    part1_sum += int(running_number)
                running_number = ""
                if (
                    is_symbol(lines[i - 1][j])
                    or is_symbol(lines[i][j])
                    or is_symbol(lines[i + 1][j])
                ):
                    has_symbol = True
                else:
                    has_symbol = False
            if ch.isdigit():
                running_number += ch
                if is_symbol(lines[i - 1][j]) or is_symbol(lines[i + 1][j]):
                    has_symbol = True
    print(f"part 1: {part1_sum}")

    part2_sum = 0
    for i, line in enumerate(lines):
        if i == 0 or i == n_rows - 1:
            continue
        for j, ch in enumerate(line):
            if is_symbol(ch):
                numbers = get_surrounding_numbers(i, j, lines)
                if len(numbers) == 2:
                    part2_sum += numbers[0] * numbers[1]
    print(f"part 2: {part2_sum}")
