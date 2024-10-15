from pathlib import Path

input_path = Path("./input")


def is_symbol(ch):
    """
    Determines if a given character is a symbol, considering it as a symbol if it
    is not a digit and not a decimal point.

    Args:
        ch (str): Representing a character, typically a single Unicode code point,
            that is being evaluated to determine if it is a symbol.

    Returns:
        bool: True if the input character is not a digit or a decimal point, and
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
    Returns a list of digits surrounding a given position in a 2D grid of lines.
    It checks the immediate neighbors (up, down, left, right) and their diagonals
    for digits.

    Args:
        i (int): Used to identify the row index in the `lines` list, where `lines`
            is a list of strings, each representing a row in a grid.
        j (int): Used to represent the column index of a 2D list `lines`. It
            determines the position of a number in the grid.
        lines (List[List[str]]): Representing a 2D list of strings, where each
            inner list represents a line in a grid, and each string represents a
            character in that line.

    Returns:
        List[int]: A list of integers representing the numbers surrounding a given
        position in a 2D list of strings.

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
