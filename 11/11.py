import numpy as np

INPUT = "input"


def expand_space(space):
    """
    Inserts empty rows and columns into a given 2D NumPy array (`space`) to maintain
    a contiguous structure. It identifies and fills gaps in rows and columns based
    on the presence of zeros and ones, respectively.

    Args:
        space (numpy.ndarray): Interpreted as a 2D array of shape (m, n) where m
            and n are the number of rows and columns respectively.

    Returns:
        Tuple[List[int],List[int]]: A list of indices where rows have been added
        and a list of indices where columns have been added to the 2D NumPy array.

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
    Calculates the Manhattan distance between two points in a grid, taking into
    account rows and columns that are expanded by a specified factor.

    Args:
        pos1 (Tuple[int, int]): Representing the coordinates of a point in a grid
            or matrix, where the first element of the tuple is the row number and
            the second element is the column number.
        pos2 (Tuple[int, int]): Represented as a pair of coordinates, where the
            first element is the row index and the second element is the column index.
        expansion_rows (List[int]): Represented as a list of integer row indices
            where additional distance is applied.
        expansion_columns (List[int]): Used to store the column indices where
            expansion occurs. It is used in conjunction with `expansion_rows` to
            determine the number of expansions between two positions.
        expansion_factor (float): Used to determine the weight of the expansions
            between the two positions.

    Returns:
        int: The total cost of movement between two positions, including both
        horizontal and vertical movement, and the cost of moving through expansion
        rows and columns.

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
    Calculates the total distance between all pairs of 1s in a given 2D space,
    considering an expanded space with increased dimensions.

    Args:
        space (Any): Expected to be a two-dimensional NumPy array.
        expansion_factor (float): Used in the `distance` function to calculate the
            distance between two points in the space, taking into account the
            expansion of the space.

    Returns:
        float: The sum of the distances between all pairs of occupied positions
        in the input space, where the distance is calculated using the provided
        expansion factor and the expanded space.

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
