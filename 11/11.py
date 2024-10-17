import numpy as np

INPUT = "input"


def expand_space(space):
    """
    Inserts rows and columns into a given 2D array (`space`) to maintain a contiguous
    structure, ensuring that rows and columns contain at least one non-zero element.

    Args:
        space (np.ndarray): Represented as a 2D array where each element is either
            0 or 1.

    Returns:
        Tuple[List[int],List[int]]: A list of integers representing the indices
        of rows and columns that were added to the input array `space` to ensure
        it contains no zeros.

    """
    expansion_rows = []
    # test
    expansion_columns = []
    for i in range(space.shape[0] - 1, -1, -1):
        if space[i, :].sum() == 0:
            space = np.insert(space, i, np.zeros((space.shape[1])), 0)
            expansion_rows.append(i)
    for j in range(space.shape[1] - 1, -1, -1):
        if (space[:, j] == 1).sum() == 0:
            space = np.insert(space, j, np.zeros((space.shape[0])), 1)
            expansion_columns.append(j)
    return expansion_rows, expansion_columns


def distance(pos1, pos2, expansion_rows, expansion_columns, expansion_factor):
    """
    Calculates the Manhattan distance between two positions with an additional
    factor for rows and columns that have been expanded, where the expansion factor
    is applied to the number of expanded positions between the two points.

    Args:
        pos1 (Tuple[int, int]): Represented as a pair of integers, where the first
            integer represents a row position and the second integer represents a
            column position.
        pos2 (Tuple[int, int]): Represented as a pair of integers, where the first
            integer is the row position and the second integer is the column position.
        expansion_rows (List[int]): Represented as a list of integers, where each
            integer represents a row in a grid that is considered an expansion area.
        expansion_columns (List[int]): Used to determine the number of columns in
            a grid that are considered as obstacles or barriers, affecting the
            distance calculation.
        expansion_factor (float): Used to calculate the weighted contribution of
            expansions to the total distance between two positions. It represents
            a factor by which the expansion count is multiplied.

    Returns:
        int: Calculated based on the Manhattan distance between two positions,
        plus the number of expansions between them, adjusted by an expansion factor.

    """
    row_expansions_between = len(
        [1 for x in range(pos1[0], pos2[0]) if x in expansion_rows]
    )
    column_expansions_between = len(
        [
            1
            for x in range(min(pos1[1], pos2[1]), max(pos1[1], pos2[1]))
            if x in expansion_columns
        ]
    )
    expansions_between = row_expansions_between + column_expansions_between
    return (
        abs(pos1[0] - pos2[0])
        + abs(pos1[1] - pos2[1])
        + (expansion_factor - 1) * expansions_between
    )


def sum_distances(space, expansion_factor):
    """
    Calculates the sum of distances between all pairs of 1s in a given 2D space,
    taking into account expansion factors for rows and columns.

    Args:
        space (numpy.ndarray): Expected to represent a 2D grid where 1 indicates
            a point of interest and 0 indicates an empty space.
        expansion_factor (float): Passed to the `distance` function. It is used
            to calculate the distance between two points in the expanded space.

    Returns:
        float: The sum of distances between all pairs of occupied positions in the
        input space, excluding pairs where the first position is above or to the
        right of the second position.

    """
    expansion_rows, expansion_columns = expand_space(space)
    running_sum = 0
    for pos1 in np.ndindex(space.shape):
        if space[pos1] == 1:
            for pos2 in np.ndindex(space.shape):
                if space[pos2] == 1:
                    if pos1[0] > pos2[0]:
                        continue
                    if pos1[0] == pos2[0] and pos1[1] >= pos2[1]:
                        continue
                    else:
                        running_sum += distance(
                            pos1,
                            pos2,
                            expansion_rows,
                            expansion_columns,
                            expansion_factor,
                        )
    return running_sum


if __name__ == "__main__":
    space = np.array(
        [
            list(x.replace(".", "0").replace("#", "1").strip())
            for x in open(INPUT).readlines()
        ]
    ).astype(int)
    print(f"part 1: {sum_distances(space, 1)}")
    print(f"part 2: {sum_distances(space, 1000000)}")
