import numpy as np

INPUT = "input"


def parse(pattern_str):
    """
    Transforms a string representation of a binary pattern into a 2D numpy array.
    It replaces "." with "0" and "#" with "1", splits the string into lines,
    converts each line into a list, and finally converts the lists into a numpy
    array of integers.

    Args:
        pattern_str (str | List[str]): Transformed into a 2D list by splitting
            each line with a newline character, replacing dots with zeros, and
            replacing hashes with ones.

    Returns:
        npndarray: A 2D array representing the input pattern string, with dots
        replaced by zeros and hashes replaced by ones.

    """
    pattern_str = [
        list(x) for x in pattern_str.replace(".", "0").replace("#", "1").split("\n")
    ]
    pattern = np.array(pattern_str, dtype=int)
    return pattern

def reflection_criterion(array1, array2, part):
    """
    Checks if two input arrays are identical or differ by exactly one element,
    depending on the specified part.

    Args:
        array1 (numpy.ndarray): Expected to be a one-dimensional array of numerical
            values.
        array2 (numpy.ndarray): Used as a reference for comparison with `array1`
            to determine whether the reflection criterion is met.
        part (int): Used to determine which reflection criterion to apply. It can
            take values 1 or 2, where 1 checks for exact equality and 2 checks if
            the absolute difference between the elements of the two arrays is 1.

    Returns:
        bool|None: True if the arrays match exactly (part 1), or if the absolute
        difference between corresponding elements in the arrays sums to 1 (part
        2), otherwise None is returned.

    """
    if part == 1:
        return (array1 == array2).all()
    if part == 2:
        return np.absolute(array1 - array2).sum() == 1


def check_reflections(pattern: np.ndarray, axis: int, part: int) -> bool:
    """
    Calculates a score based on the presence of reflections in a given pattern
    along its axes. It iterates over the pattern, checks for reflections at each
    position, and returns the total score if a reflection is found.

    Args:
        pattern (np.ndarray): Represented by a 2D numpy array, which is a
            multi-dimensional array of numerical values.
        axis (int): Used to specify the axis along which the reflection check is
            performed. It can have two possible values: 0 or 1.
        part (int): Passed to the `reflection_criterion` function, which is used
            to determine whether the reflection criterion is met for the arrays
            `before_array` and `after_array`.

    Returns:
        bool: True if the pattern exhibits reflections based on the specified
        criterion, and False otherwise.

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

