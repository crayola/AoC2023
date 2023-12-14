import numpy as np

INPUT = "input"


def parse(pattern_str):
    pattern_str = [
        list(x) for x in pattern_str.replace(".", "0").replace("#", "1").split("\n")
    ]
    pattern = np.array(pattern_str, dtype=int)
    return pattern

def reflection_criterion(array1, array2, part):
    if part == 1:
        return (array1 == array2).all()
    if part == 2:
        return np.absolute(array1 - array2).sum() == 1


def check_reflections(pattern: np.ndarray, axis: int, part: int) -> bool:
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

