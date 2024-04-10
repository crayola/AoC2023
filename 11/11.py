import numpy as np

INPUT = "input"


def expand_space(space):
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
