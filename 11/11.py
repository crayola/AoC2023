import numpy as np

INPUT = "input"


def expand_space(space):
    """
    Adds rows and columns to a given 2D array (`space`) to fill in gaps where all
    elements are zero, preserving the original data and their positions.

    Args:
        space (ndarray): Represented as a 2D array of integers, where 0 typically
            denotes an empty space and 1 denotes a filled space, with the shape
            of the array representing the dimensions of the space.

    Returns:
        Tuple[List[int],List[int]]: A pair of lists containing indices of rows and
        columns that were inserted to expand the input 2D array.

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
    Calculates the Manhattan distance between two points, taking into account
    additional "expansion" rows and columns with a given factor. It includes the
    distance between the points and the expanded areas, weighted by the expansion
    factor.

    Args:
        pos1 (Tuple[int, int]): Used to represent the coordinates of a position
            in a grid, where the first element is the row number and the second
            element is the column number.
        pos2 (Tuple[int, int]): Represented as a pair of coordinates in a
            two-dimensional space, where the first element is the row position and
            the second element is the column position.
        expansion_rows (List[int]): Representing a list of rows where expansions
            occur, likely affecting the distance calculation.
        expansion_columns (List[int]): Used to calculate the number of columns
            between two positions that are part of the grid expansion. It contains
            indices of the columns that are expanded.
        expansion_factor (float): Used to calculate a weighted penalty for traversing
            through expanded rows and columns.

    Returns:
        int: A weighted Manhattan distance between two points, taking into account
        rows and columns with expansions.

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
    Calculates the total distance between all pairs of points in a given 2D space,
    where points are represented as 1's in a numpy array, and distances are
    calculated using the `distance` function, considering an expanded space with
    a specified expansion factor.

    Args:
        space (ndarray): 2D, representing a grid or matrix where each element is
            a point in space, with a value of 1 indicating the presence of a point.
        expansion_factor (float): Used in the `distance` function to calculate the
            distance between two points in the expanded space.

    Returns:
        int: The sum of distances between all pairs of 1's in a 2D grid, where the
        distance between two points is calculated using the `distance` function,
        taking into account the expansion of the space and a specified factor.

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
