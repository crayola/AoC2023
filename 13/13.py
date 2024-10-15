import numpy as np

INPUT = "input"


def parse(pattern_str):
    """
    Converts a string representing a binary pattern into a 2D NumPy array. It
    replaces dots with zeros and hashes with ones, splits the string into lines,
    and converts each line into a list of integers before creating a 2D NumPy array.

    Args:
        pattern_str (str | List[str]): Expected to be a string representing a
            pattern, with each line representing a row in the pattern. The string
            can contain '.' and '#' characters, which are replaced with '0' and
            '1' respectively.

    Returns:
        numpyndarray: A 2D array of integers, representing a pattern matrix created
        from the input string.

    """
    pattern_str = [
        list(x) for x in pattern_str.replace(".", "0").replace("#", "1").split("\n")
    ]
    pattern = np.array(pattern_str, dtype=int)
    return pattern

def reflection_criterion(array1, array2, part):
    """
    Determines whether two input arrays satisfy a specific criterion based on the
    `part` parameter. For `part` 1, it checks if the two arrays are identical
    element-wise. For `part` 2, it checks if the absolute difference between
    corresponding elements is exactly 1.

    Args:
        array1 (np.ndarray): Used as a reference array for comparison with `array2`
            in the function's two possible scenarios.
        array2 (np.ndarray): Used as a comparison element to evaluate the criterion
            specified by the value of the `part` parameter.
        part (int): Used to specify the reflection criterion. It can have two
            possible values: 1 and 2, which correspond to different reflection criteria.

    Returns:
        bool|npndarray: Either True or False, depending on the input parameters.

    """
    if part == 1:
        return (array1 == array2).all()
    if part == 2:
        return np.absolute(array1 - array2).sum() == 1


def check_reflections(pattern: np.ndarray, axis: int, part: int) -> bool:
    """
    Evaluates the degree of reflection in a given 2D array `pattern` along both
    axes. It calculates a score based on the number of positions where the pattern
    reflects itself, with higher scores indicating more significant reflections.

    Args:
        pattern (np.ndarray*): Represented as a numerical array, likely a 2D or
            3D array, where each axis represents a dimension in space.
        axis (int*): Interpreted as the dimension along which the pattern's
            reflection is being checked.
        part (int*): Used in the `reflection_criterion` function, which is not
            shown here, to determine whether the arrays before and after the current
            position `i` meet the reflection criterion.

    Returns:
        bool*: True if the pattern has a reflection at any position, and False otherwise.

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

