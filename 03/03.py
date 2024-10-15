from pathlib import Path

input_path = Path("./input")


def is_symbol(ch):
    """
    Determines whether a given character is a symbol by checking if it is not a
    digit and not a decimal point. It returns `True` for all other characters,
    indicating they are symbols.

    Args:
        ch (str): Representing a single character.

    Returns:
        bool: True if the input character is not a digit or a dot, and False otherwise.

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
    Returns a list of numbers found in the surrounding cells of a given position
    `(i, j)` within a 2D grid of lines, considering both horizontal and vertical
    neighbors, as well as diagonals when the immediate horizontal or vertical
    neighbors are not numbers.

    Args:
        i (int): Used to represent the row index of a grid of numbers, where the
            top row is at index 0.
        j (int): Used as the column index in the 2D list `lines` to access elements
            at a specific x-coordinate.
        lines (List[List[str]]): Representing a 2D grid of strings, where each
            string is a character or digit from a text representation of a Sudoku
            puzzle.

    Returns:
        List[int]: A list of integers representing the numbers surrounding a given
        position in a 2D grid, excluding non-digit characters.

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
