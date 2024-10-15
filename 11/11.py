import numpy as np

INPUT = "input"


def expand_space(space):
    """
    Inserts new rows or columns at the beginning of a given 2D array (space) to
    accommodate empty spaces, as indicated by zeros or empty columns. It maintains
    the original array's structure while expanding it to accommodate new elements.

    Args:
        space (ndarray): Expected to be a 2D array of shape (n_rows, n_cols), where
            n_rows and n_cols are positive integers, representing a grid of binary
            values.

    Returns:
        Tuple[List[int],List[int]]: A tuple containing two lists: `expansion_rows`
        and `expansion_columns`. Each list contains integers representing the
        indices of rows and columns that were inserted during the expansion process.

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
    Calculates the Manhattan distance between two points, taking into account rows
    and columns that have been expanded, and applying a factor to the number of
    expansions between the two points.

    Args:
        pos1 (Tuple[int, int]): Represented as a pair of integers, where the first
            integer represents a row position and the second integer represents a
            column position.
        pos2 (Tuple[int, int]): Represented as a pair of integers, where the first
            integer is the row position and the second integer is the column position.
        expansion_rows (List[int]): Used to store row indices where expansion occurs.
        expansion_columns (List[int]): Represented as a set of column indices where
            expansion is possible.
        expansion_factor (float): Used to calculate the penalty for traversing
            through expanded cells. The penalty is calculated as `(expansion_factor
            - 1) * expansions_between`, where `expansions_between` is the number
            of expanded cells between the two positions.

    Returns:
        int: Representative of the total cost of moving from position `pos1` to
        position `pos2`, taking into account both the absolute difference in
        position and the number of expansions encountered.

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
    Calculates the total distance between all pairs of occupied cells in a given
    space, excluding pairs where the first cell is to the right or directly above
    the second cell.

    Args:
        space (ndarray): A 2D grid of integers, where 1 represents a point of
            interest and 0 represents an empty space.
        expansion_factor (float): Used in the `distance` function call to calculate
            the distance between two positions in the space.

    Returns:
        int: The total sum of distances between all pairs of cells in the input
        `space` array that contain the value 1, calculated with the given `expansion_factor`.

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
