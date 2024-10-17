import numpy as np

INPUT = "input"


def parse(pattern_str):
    """
    Transforms a string representing a pattern into a 2D NumPy array. It replaces
    dots with zeros and hashes with ones, then splits the string into lines and
    converts each line into a list of integers.

    Args:
        pattern_str (str): Expected to be a multiline string representing a binary
            pattern, where '.' is replaced with '0' and '#' with '1'.

    Returns:
        npndarray: A two-dimensional array of integers, where each integer represents
        a pixel in a binary image, with 0 indicating a background pixel and 1
        indicating a foreground pixel.

    """
    pattern_str = [
        list(x) for x in pattern_str.replace(".", "0").replace("#", "1").split("\n")
    ]
    pattern = np.array(pattern_str, dtype=int)
    return pattern

def reflection_criterion(array1, array2, part):
    """
    Determines whether two input arrays satisfy a specific criterion based on their
    reflection. It checks if the arrays are identical or if their absolute difference
    sums to 1, depending on the specified part.

    Args:
        array1 (ndarray): Used as one of the two input arrays for comparison
            purposes. It is expected to be a numpy array.
        array2 (ndarray): Expected to be a numpy array.
        part (int): Used to specify the reflection criterion to be applied. It can
            take two values: 1, indicating an element-wise equality check, and 2,
            indicating a check for a single element-wise difference of absolute
            value 1.

    Returns:
        bool: True if the arrays are identical, and False otherwise for part 1, and
        True if the absolute difference between the arrays sums up to 1, and False
        otherwise for part 2.

    """
    if part == 1:
        return (array1 == array2).all()
    if part == 2:
        return np.absolute(array1 - array2).sum() == 1


def check_reflections(pattern: np.ndarray, axis: int, part: int) -> bool:
    """
    Scores the presence of reflections in a 2D array (`np.ndarray`), based on a
    given `part`. It does this by checking each element against its reflection
    across both the x and y axes, using a custom `reflection_criterion` function.

    Args:
        pattern (np.ndarray): Represented as a multi-dimensional array of numerical
            values.
        axis (int): Used to specify the dimension along which the pattern is checked
            for reflections.
        part (int): Used by the `reflection_criterion` function to evaluate the
            reflection of two sub-arrays.

    Returns:
        bool: True if the pattern exhibits specified reflections and False otherwise.

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

