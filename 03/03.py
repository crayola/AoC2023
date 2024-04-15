from pathlib import Path

input_path = Path("./input")


def is_symbol(ch):
    """
    determines whether a given character is a digit or ".". It returns `True` if
    it is not a digit, and `False` otherwise.

    Args:
        ch (str): character to be tested for symbolicity.

    Returns:
        bool: a boolean value indicating whether the given character is a symbol
        or not.

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
    computes and returns an list of numbers that surround a given number within a
    grid of lines and columns, based on neighboring cells marked as digits or non-digits.

    Args:
        i (int): 2D coordinate of the current cell being analyzed.
        j (int): 2D coordinate of the cell where the number is sought within the
            grid.
        lines (ndarray (i.e., an array-like object).): 2D grid of integers to
            search for surrounded numbers, and it is used to determine the adjacent
            numbers to search for in each position of the grid.
            
            		- Lines is an array of arrays, representing a 2D matrix of numbers.
            		- Each line in the array represents a sequence of digits.
            		- The indices `i`, `j`, and `k` denote positions within the line and
            matrix respectively.
            		- The function iteratively checks if the neighboring elements are
            also digits, and appends them to the resulting list of surrounding
            numbers if they are.
            

    Returns:
        list: a list of numbers found within a given cell and its neighbors.

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
