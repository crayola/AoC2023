INPUT = "input"
S_TILE = "|"


def find_next(previous, current, lines):
    tile = lines[current[0]][current[1]]

    if tile == "|":
        return (current[0] + current[0] - previous[0], current[1])
    elif tile == "-":
        return (current[0], current[1] + current[1] - previous[1])
    elif tile == "L":
        if previous[0] < current[0]:  # from up
            return (current[0], current[1] + 1)
        else:  # from right
            return (current[0] - 1, current[1])
    elif tile == "J":
        if previous[0] < current[0]:  # from up
            return (current[0], current[1] - 1)
        else:  # from left
            return (current[0] - 1, current[1])
    elif tile == "7":
        if previous[0] > current[0]:  # from down
            return (current[0], current[1] - 1)
        else:
            return (current[0] + 1, current[1])  # from left
    elif tile == "F":
        if previous[0] > current[0]:  # from down
            return (current[0], current[1] + 1)
        else:  # from right
            return (current[0] + 1, current[1])
    else:
        raise Exception()


if __name__ == "__main__":
    lines = [x.strip() for x in open(INPUT).readlines()]

    for i_start, line in enumerate(lines):
        try:
            j_start = line.index("S")
            break
        except Exception:
            pass

    previous = (i_start, j_start)
    current = find_next(previous, (i_start + 1, j_start), lines)
    loop_tiles = {previous, current, (i_start + 1, j_start)}
    previous = (i_start + 1, j_start)
    i = 1
    while current != (i_start, j_start):
        i += 1
        next = find_next(previous, current, lines)
        loop_tiles.add(next)
        previous, current = current, next

    print(f"part 1: {i // 2 + 1}")

    part2 = 0

    in_L = 0
    in_F = 0

    for i, line in enumerate(lines):
        count = 0
        [pos[1] for pos in loop_tiles if pos[0] == i]
        for j, c in enumerate(line):
            if c == "S":
                c = S_TILE
            if (i, j) in loop_tiles:
                if c == "|":
                    count += 1
                if c == "L":
                    in_L = True
                if c == "F":
                    in_F = True
                if c == "J":
                    if in_F:
                        count += 1
                        in_F = 0
                    if in_L:
                        in_L = 0
                if c == "7":
                    if in_F:
                        in_F = 0
                    if in_L:
                        count += 1
                        in_L = 0
            elif count % 2 == 1:
                part2 += 1
    print(f"part 2: {part2}")
