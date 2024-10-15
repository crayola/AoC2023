import numpy as np

INPUT = "input"


def parse(pattern_str):
    """
    Transforms a string pattern into a 2D NumPy array by replacing "." with "0",
    "#" with "1", splitting the string into lines, converting each line into a
    list, and then into a 1D array, which is converted into a 2D array.

    Args:
        pattern_str (str | List[str]): Preprocessed to remove newline characters,
            replace "." with "0", and replace "#" with "1". Resulting in a 2D list
            where each inner list represents a row in the pattern.

    Returns:
        npndarray[int]: An array of integers representing a pattern, where 0s and
        1s are used to denote empty and occupied spaces, respectively.

    """
    pattern_str = [
        list(x) for x in pattern_str.replace(".", "0").replace("#", "1").split("\n")
    ]
    pattern = np.array(pattern_str, dtype=int)
    return pattern

def reflection_criterion(array1, array2, part):
    """
    Checks whether two input arrays meet specific conditions based on the value
    of `part`. It returns True if the arrays are identical (part 1) or differ by
    exactly one element (part 2), and False otherwise.

    Args:
        array1 (numpy.ndarray): Expected to be a one-dimensional array, likely
            representing a sequence of numerical values.
        array2 (numpy.ndarray): Used in comparisons to determine the reflection
            criterion. It is expected to be a one-dimensional array of numerical
            values, likely representing a signal or data.
        part (int): Used to determine the type of reflection criterion to apply.
            It can have values of 1 or 2, corresponding to element-wise equality
            and absolute difference summation, respectively.

    Returns:
        bool: True if the input arrays are identical when `part` equals 1, and
        True if the absolute difference between the input arrays sums up to 1 when
        `part` equals 2.

    """
    if part == 1:
        return (array1 == array2).all()
    if part == 2:
        return np.absolute(array1 - array2).sum() == 1


def check_reflections(pattern: np.ndarray, axis: int, part: int) -> bool:
    """
    Calculates a score based on the presence of reflections in a given pattern
    along specified axes. It iterates over the pattern, checking for reflections
    at each position, and increments the score accordingly.

    Args:
        pattern (np.ndarray*): Expected to be a two-dimensional NumPy array.
        axis (int*): Restricted to values 0 and 1, indicating that the function
            operates on either the rows or the columns of the input array, depending
            on the axis value.
        part (int*): Used in the `reflection_criterion` function, which is not
            shown in the code snippet, indicating that it is likely used to determine
            the reflection criterion for the current pattern part.

    Returns:
        bool*: True if the input pattern exhibits reflection symmetry at any axis,
        False otherwise.

    """
    score = 0
    for axis in [0,1]:
        length = pattern.shape[axis]
        for i in range(1, length):
            before_array = pattern.take(
                range(max(0, 2 * i - length), i), axis=axis
            )
            after_array = pattern.take(range(min(2 * i - 1, length - 1), i-1, -1), axis=axis)
            if reflection_criterion(before_array, after_array, part):
                score += i * (1 if axis == 1 else 100)
                break
    return score



if __name__ == "__main__":
    patterns_str = open(INPUT).read().split("\n\n")
    patterns = [parse(pat) for pat in patterns_str]

    part1 = 0
    for pat in patterns:
        part1 += check_reflections(pat, 1, 1)
    print(f"part1: {part1}")


    part2 = 0
    for pat in patterns:
        part2 += check_reflections(pat, 1,2)
    print(f"part2: {part2}")

